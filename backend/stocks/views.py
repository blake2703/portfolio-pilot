from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
import yfinance as yf
from ..models.users import User
from ..models.stocks import Stock
from http import HTTPStatus
from ..utils import db

stocks_namespace = Namespace('stocks', description="Stocks namespace")

stock_model = stocks_namespace.model(
    'Stocks',
    {
        'ticker': fields.String(required=True, description="Ticker"),
        'quantity': fields.Float(required=True, description="Updated quantity"),
        'average_price': fields.Float(required=True, description="Updated average price")
    }
)

delete_stock_model = stocks_namespace.model(
    'Stocks',
    {
        'ticker': fields.String(required=True, description="Ticker"),
    }
)

# register route
@stocks_namespace.route('/stocks/')
class AddGetUpdateDelete(Resource):
    
    # expect add stock model as input
    @stocks_namespace.expect(stock_model)
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
            quantity=data.get('quantity'),
            average_price=data.get('average_price'),
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
            "quantity": new_stock.quantity,
            "average_price": new_stock.average_price,
            "user_id": new_stock.user_id
        }, HTTPStatus.CREATED
    
    @jwt_required(refresh=True)
    def get(self):
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        
        holdings = Stock.query.filter_by(user_id=current_user.id).all()
        
        holdings_to_json = [
            {
                'ticker': stock.ticker,
                'company_name': stock.company_name,
                'sector': stock.sector,
                'industry': stock.industry,
                'quantity': stock.quantity,
                'average_cost': stock.average_price
            }
            for stock in holdings
        ]
        
        return holdings_to_json, HTTPStatus.OK

    @stocks_namespace.expect(delete_stock_model)
    @jwt_required(refresh=True)
    def delete(self):
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        
        data = request.get_json()
        ticker = data.get('ticker')
        
        stock = Stock.query.filter_by(user_id=current_user.id, ticker=ticker).first()
        
        if not stock:
            return {"message": "Stock not found"}, HTTPStatus.NOT_FOUND

        stock.delete()
        
        return {"message": f"Stock {ticker} deleted successfully"}, HTTPStatus.OK
    
    @stocks_namespace.expect(stock_model)
    @jwt_required(refresh=True)
    def put(self):
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        
        data = request.get_json()
        ticker = data.get('ticker')
        
        order_to_update = Stock.query.filter_by(user_id=current_user.id, ticker=ticker).first()
        order_to_update.quantity = data.get('quantity')
        order_to_update.average_price = data.get('average_price')
        db.session.commit()
        
        return {
            "message": f"Stock {ticker} has been updated with a quantity of {order_to_update.quantity} and average price of {order_to_update.average_price}"}, HTTPStatus.OK        