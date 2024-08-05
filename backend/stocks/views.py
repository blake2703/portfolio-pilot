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

@stocks_namespace.route('/add-stock')
class AddStock(Resource):
    
    @stocks_namespace.expect(add_stock_model)
    @jwt_required()
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
            industry=stock_data.get('industry', ''),  # Assuming this is the correct field name in your model
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
        
        
        
        
        
        