from app import create_app
import os

# 환경 설정
config_name = os.getenv('FLASK_ENV', 'default')

# Flask 애플리케이션 생성
app = create_app(config_name)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['FLASK_DEBUG']
    )
