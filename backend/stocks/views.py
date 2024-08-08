from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
import yfinance as yf
from ..models.users import User
from ..models.stocks import Stock
from http import HTTPStatus

stocks_namespace = Namespace('stocks', description="Stocks namespace")

add_stock_model = stocks_namespace.model(
    'Stocks',
    {
        'ticker': fields.String(required=True, description="Ticker"),
    }
)

# register route
@stocks_namespace.route('/stocks/')
class AddStock(Resource):
    
    # expect add stock model as input
    @stocks_namespace.expect(add_stock_model)
    # give access through refresh token
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        
        data = request.get_json()
        ticker = data.get('ticker')
        
        stock = yf.Ticker(ticker=ticker)
        stock_data = stock.info
        
        new_stock = Stock(
            ticker=ticker,
            company_name=stock_data.get('shortName', ''),
            sector=stock_data.get('sector', ''),
            industry=stock_data.get('industry', ''),
            user_id=current_user.id  # Associate stock with the user
        )
        
        new_stock.save()
        
        # Serialize the Stock object into a dictionary
        return {
            "id": new_stock.id,
            "ticker": new_stock.ticker,
            "company_name": new_stock.company_name,
            "sector": new_stock.sector,
            "industry": new_stock.industry,
            "user_id": new_stock.user_id
        }, HTTPStatus.CREATED