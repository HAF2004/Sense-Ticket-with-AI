# app_v2.py
# Enhanced Flask dashboard with API endpoints and control panel

from flask import Flask, render_template, jsonify, request
from models.database import db_manager, Message, AIResponse, ChannelSettings, BotStatus, Action
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import analysis

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def dashboard():
    """
    Main dashboard page
    """
    session = db_manager.get_session()
    
    try:
        # Get statistics
        total_messages = session.query(Message).count()
        total_ai_responses = session.query(AIResponse).count()
        total_actions = session.query(Action).count()
        unique_users = session.query(func.count(func.distinct(Message.author_id))).scalar()
        
        # Bot status
        bot_status = session.query(BotStatus).first()
        if bot_status and bot_status.last_heartbeat:
            time_diff = (datetime.utcnow() - bot_status.last_heartbeat).total_seconds()
            is_online = time_diff < 120  # Online if heartbeat within 2 minutes
        else:
            is_online = False
        
        # Recent conversations (20 for initial load)
        recent_convs = session.query(Message).order_by(desc(Message.timestamp)).limit(20).all()
        
        stats = {
            'total_conversations': total_messages,
            'total_ai_responses': total_ai_responses,
            'total_actions': total_actions,
            'unique_users': unique_users,
            'bot_status': 'Online' if is_online else 'Offline'
        }
        
        recent_conversations = [{
            'user_id': msg.author_id,
            'content': msg.content[:100],
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_ai': msg.is_ai_response,
            'category': 'AI' if msg.is_ai_response else 'User'
        } for msg in recent_convs]
        
        # Calculate clustering for initial load
        clustering_data = None
        try:
            import analysis
            result = analysis.perform_clustering()
            if result and result.get('status') == 'success':
                # Count users per cluster
                clusters = {}
                for item in result['data']:
                    c = item['cluster']
                    clusters[c] = clusters.get(c, 0) + 1
                clustering_data = {
                    'labels': [f'Cluster {k}' for k in sorted(clusters.keys())],
                    'values': [clusters[k] for k in sorted(clusters.keys())]
                }
        except Exception as e:
            print(f"Clustering error: {e}")
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             recent_conversations=recent_conversations,
                             clustering=clustering_data)
        
    finally:
        session.close()


@app.route('/api/discord/stats')
def api_stats():
    """
    API endpoint for statistics
    """
    session = db_manager.get_session()
    
    try:
        # Today's stats
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        ai_messages_today = session.query(Message).filter(
            Message.is_ai_response == True,
            Message.timestamp >= today_start
        ).count()
        
        member_messages_today = session.query(Message).filter(
            Message.is_bot == False,
            Message.timestamp >= today_start
        ).count()
        
        # Top channels
        top_channels = session.query(
            Message.channel_id,
            func.count(Message.id).label('count')
        ).group_by(Message.channel_id).order_by(desc('count')).limit(5).all()
        
        # Average response length
        avg_length = session.query(func.avg(func.length(Message.content))).filter(
            Message.is_ai_response == True
        ).scalar() or 0
        
        return jsonify({
            'ai_messages_today': ai_messages_today,
            'member_messages_today': member_messages_today,
            'top_channels': [{'channel_id': ch[0], 'count': ch[1]} for ch in top_channels],
            'avg_response_length': round(avg_length, 2)
        })
        
    finally:
        session.close()


@app.route('/api/discord/ai/logs')
def api_ai_logs():
    """
    API endpoint for AI conversation logs with pagination
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    session = db_manager.get_session()
    
    try:
        # Get AI responses with messages
        ai_responses = session.query(AIResponse).order_by(
            desc(AIResponse.created_at)
        ).offset((page - 1) * per_page).limit(per_page).all()
        
        logs = []
        for ai_resp in ai_responses:
            logs.append({
                'id': ai_resp.id,
                'request': ai_resp.request_message.content if ai_resp.request_message else '',
                'response': ai_resp.response_message.content if ai_resp.response_message else '',
                'feedback_score': ai_resp.feedback_score,
                'confidence': ai_resp.confidence_score,
                'timestamp': ai_resp.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        total = session.query(AIResponse).count()
        
        return jsonify({
            'logs': logs,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
        
    finally:
        session.close()


@app.route('/api/discord/control/toggle', methods=['POST'])
def api_toggle_ai():
    """
    API endpoint to toggle AI per channel
    """
    data = request.json
    channel_id = data.get('channel_id')
    enabled = data.get('enabled', True)
    ai_mode = data.get('ai_mode', 'mention_only')
    
    if not channel_id:
        return jsonify({'error': 'channel_id required'}), 400
    
    session = db_manager.get_session()
    
    try:
        # Get or create channel settings
        settings = session.query(ChannelSettings).filter_by(
            channel_id=channel_id
        ).first()
        
        if settings:
            settings.ai_enabled = enabled
            settings.ai_mode = ai_mode
            settings.updated_at = datetime.utcnow()
        else:
            settings = ChannelSettings(
                channel_id=channel_id,
                guild_id=data.get('guild_id', 'unknown'),
                ai_enabled=enabled,
                ai_mode=ai_mode
            )
            session.add(settings)
        
        session.commit()
        
        return jsonify({
            'success': True,
            'channel_id': channel_id,
            'ai_enabled': enabled,
            'ai_mode': ai_mode
        })
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
        
    finally:
        session.close()


@app.route('/api/discord/control/flush', methods=['POST'])
def api_flush_cache():
    """
    API endpoint to flush AI cache
    """
    try:
        # Clear analysis cache if exists
        if hasattr(analysis, 'clear_cache'):
            analysis.clear_cache()
        
        return jsonify({
            'success': True,
            'message': 'Cache flushed successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/conversations')
def api_conversations():
    """
    API endpoint for paginated conversations (infinite scroll)
    """
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 20, type=int)
    
    session = db_manager.get_session()
    
    try:
        messages = session.query(Message).order_by(
            desc(Message.timestamp)
        ).offset(offset).limit(limit).all()
        
        conversations = [{
            'user_id': msg.author_id,
            'content': msg.content[:100],
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_ai': msg.is_ai_response,
            'category': 'AI' if msg.is_ai_response else 'User'
        } for msg in messages]
        
        return jsonify({
            'conversations': conversations,
            'has_more': len(conversations) == limit
        })
        
    finally:
        session.close()


@app.route('/api/clustering')
def api_clustering():
    """
    API endpoint for clustering analysis
    """
    try:
        result = analysis.perform_clustering()
        if result is None:
            return jsonify({
                'status': 'not_enough_data',
                'message': 'No data available for clustering'
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Expose application for passenger_wsgi.py
application = app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
