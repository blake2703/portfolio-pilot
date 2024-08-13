from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
import yfinance as yf
from ..models.users import User
from ..models.stocks import Stock
from http import HTTPStatus
from ..utils import db
from .sharpe import Sharpe
from .sortino import Sortino
import numpy as np

metrics_namespace = Namespace('metrics', description="Metrics namespace")


@metrics_namespace.route('/sharpe')
class SharpeEndpoint(Resource):
    
    @jwt_required(refresh=True)
    def get(self):
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        
        holdings = Stock.query.filter_by(user_id=current_user.id).all()
        ticker_list = [holding.ticker for holding in holdings]
        
        s = Sharpe(ticker_list=ticker_list)
        
        weights, yearly_returns, yearly_volatility, sharpe_ratio = s.calc_statistics()
        
        # Convert numpy arrays to lists
        if isinstance(weights, np.ndarray):
            weights = weights.tolist()
        else:
            weights
        
        if isinstance(yearly_returns, np.float64):
            yearly_returns = float(yearly_returns)
        else:
            yearly_returns
        
        if isinstance(yearly_volatility, np.float64):
            yearly_volatility = float(yearly_volatility)
        else:
            yearly_volatility
        
        if isinstance(sharpe_ratio, np.float64):
            sharpe_ratio = float(sharpe_ratio)
        else:
            sharpe_ratio

        
        return {
            "Optimized weights": weights,
            "Yearly returns": yearly_returns,
            "Yearly volatility": yearly_volatility,
            "Sharpe ratio": sharpe_ratio
        }, HTTPStatus.OK

@metrics_namespace.route("/sortino")
class SortinoEndpoint(Resource):
    
    @jwt_required(refresh=True)
    def get(self):
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        
        holdings = Stock.query.filter_by(user_id=current_user.id).all()
        ticker_list = [holding.ticker for holding in holdings]
        
        s = Sortino(ticker_list=ticker_list)
        
        weights, yearly_returns, yearly_volatility, sharpe_ratio = s.calc_statistics()
        
        # Convert numpy arrays to lists
        if isinstance(weights, np.ndarray):
            weights = weights.tolist()
        else:
            weights
        
        if isinstance(yearly_returns, np.float64):
            yearly_returns = float(yearly_returns)
        else:
            yearly_returns
        
        if isinstance(yearly_volatility, np.float64):
            yearly_volatility = float(yearly_volatility)
        else:
            yearly_volatility
        
        if isinstance(sharpe_ratio, np.float64):
            sharpe_ratio = float(sharpe_ratio)
        else:
            sharpe_ratio

        
        return {
            "Optimized weights": weights,
            "Yearly returns": yearly_returns,
            "Yearly volatility": yearly_volatility,
            "Sharpe ratio": sharpe_ratio
        }, HTTPStatus.OK