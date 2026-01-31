"""
Forecasting and Predictive Analytics Assistant

Combines historical data with forecasting tools for domain-aware trend analysis
and strategic planning.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
from enum import Enum


class ForecastModel(Enum):
    """Available forecasting models."""
    ARIMA = "arima"
    PROPHET = "prophet"
    LSTM = "lstm"
    ENSEMBLE = "ensemble"


@dataclass
class ForecastResult:
    """Represents a forecast result."""
    metric: str
    forecast_values: List[float]
    forecast_dates: List[datetime]
    confidence_intervals: List[Tuple[float, float]]
    base_case: float
    bull_case: float
    bear_case: float
    scenario_probabilities: Dict[str, float]
    model_used: ForecastModel
    accuracy_score: float


class ForecastingAgent:
    """
    Agent for time series forecasting and predictive analytics.
    
    Features:
    - Multiple forecasting models (ARIMA, Prophet, LSTM)
    - Scenario modeling (base, bull, bear cases)
    - Confidence intervals
    - What-if analysis
    - Model ensemble and selection
    
    Example:
        >>> agent = ForecastingAgent()
        >>> forecast = agent.forecast(
        ...     metric="TVL",
        ...     historical_data=tvl_data,
        ...     periods=30
        ... )
        >>> print(f"Base case: ${forecast.base_case}B")
    """
    
    def __init__(self, default_model: ForecastModel = ForecastModel.ENSEMBLE):
        """
        Initialize Forecasting Agent.
        
        Args:
            default_model: Default forecasting model to use
        """
        self.default_model = default_model
        self.forecast_history = []
    
    def forecast(
        self,
        metric: str,
        historical_data: List[float],
        periods: int = 30,
        model: Optional[ForecastModel] = None,
        confidence_level: float = 0.95
    ) -> ForecastResult:
        """
        Generate forecast for a metric.
        
        Args:
            metric: Metric name to forecast
            historical_data: Historical time series data
            periods: Number of periods to forecast
            model: Forecasting model to use
            confidence_level: Confidence level for intervals
            
        Returns:
            ForecastResult with predictions and scenarios
        """
        model = model or self.default_model
        
        # Generate base forecast
        forecast_values = self._generate_forecast(historical_data, periods, model)
        forecast_dates = self._generate_forecast_dates(periods)
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(
            forecast_values, confidence_level
        )
        
        # Generate scenarios
        base_case = forecast_values[-1]
        bull_case = self._generate_bull_case(historical_data, forecast_values)
        bear_case = self._generate_bear_case(historical_data, forecast_values)
        
        # Calculate scenario probabilities
        scenario_probs = self._calculate_scenario_probabilities(
            historical_data, base_case, bull_case, bear_case
        )
        
        # Assess accuracy
        accuracy = self._assess_model_accuracy(historical_data, model)
        
        result = ForecastResult(
            metric=metric,
            forecast_values=forecast_values,
            forecast_dates=forecast_dates,
            confidence_intervals=confidence_intervals,
            base_case=base_case,
            bull_case=bull_case,
            bear_case=bear_case,
            scenario_probabilities=scenario_probs,
            model_used=model,
            accuracy_score=accuracy
        )
        
        self.forecast_history.append({
            'metric': metric,
            'timestamp': datetime.now(),
            'forecast': result
        })
        
        return result
    
    def what_if_analysis(
        self,
        metric: str,
        historical_data: List[float],
        scenarios: Dict[str, Dict[str, Any]]
    ) -> Dict[str, ForecastResult]:
        """
        Perform what-if analysis with different scenarios.
        
        Args:
            metric: Metric to analyze
            historical_data: Historical data
            scenarios: Dictionary of scenario parameters
            
        Returns:
            Dictionary mapping scenario names to forecasts
        """
        results = {}
        
        for scenario_name, params in scenarios.items():
            # Apply scenario parameters to historical data
            adjusted_data = self._apply_scenario_params(historical_data, params)
            
            # Generate forecast for this scenario
            results[scenario_name] = self.forecast(
                metric=metric,
                historical_data=adjusted_data,
                periods=params.get('periods', 30)
            )
        
        return results
    
    def _generate_forecast(
        self,
        historical_data: List[float],
        periods: int,
        model: ForecastModel
    ) -> List[float]:
        """
        Generate forecast using specified model.
        
        Args:
            historical_data: Historical time series
            periods: Number of periods to forecast
            model: Model to use
            
        Returns:
            List of forecasted values
        """
        if model == ForecastModel.ARIMA:
            return self._arima_forecast(historical_data, periods)
        elif model == ForecastModel.PROPHET:
            return self._prophet_forecast(historical_data, periods)
        elif model == ForecastModel.LSTM:
            return self._lstm_forecast(historical_data, periods)
        else:  # ENSEMBLE
            return self._ensemble_forecast(historical_data, periods)
    
    def _arima_forecast(self, data: List[float], periods: int) -> List[float]:
        """ARIMA model forecast (placeholder)."""
        # Placeholder: Implement ARIMA using statsmodels
        # Calculate trend and seasonality
        trend = (data[-1] - data[0]) / len(data)
        forecast = []
        last_value = data[-1]
        
        for i in range(periods):
            forecast.append(last_value + trend * (i + 1))
        
        return forecast
    
    def _prophet_forecast(self, data: List[float], periods: int) -> List[float]:
        """Prophet model forecast (placeholder)."""
        # Placeholder: Implement Prophet
        # Similar to ARIMA for now
        return self._arima_forecast(data, periods)
    
    def _lstm_forecast(self, data: List[float], periods: int) -> List[float]:
        """LSTM model forecast (placeholder)."""
        # Placeholder: Implement LSTM using PyTorch/TensorFlow
        return self._arima_forecast(data, periods)
    
    def _ensemble_forecast(self, data: List[float], periods: int) -> List[float]:
        """Ensemble forecast combining multiple models."""
        arima = self._arima_forecast(data, periods)
        prophet = self._prophet_forecast(data, periods)
        lstm = self._lstm_forecast(data, periods)
        
        # Average the forecasts
        ensemble = []
        for i in range(periods):
            avg = (arima[i] + prophet[i] + lstm[i]) / 3
            ensemble.append(avg)
        
        return ensemble
    
    def _generate_forecast_dates(self, periods: int) -> List[datetime]:
        """Generate forecast date range."""
        start_date = datetime.now()
        return [start_date + timedelta(days=i) for i in range(1, periods + 1)]
    
    def _calculate_confidence_intervals(
        self,
        forecast: List[float],
        confidence_level: float
    ) -> List[Tuple[float, float]]:
        """Calculate confidence intervals for forecast."""
        intervals = []
        
        # Simple approach: use percentage bands
        margin = (1 - confidence_level) / 2
        
        for value in forecast:
            lower = value * (1 - margin)
            upper = value * (1 + margin)
            intervals.append((lower, upper))
        
        return intervals
    
    def _generate_bull_case(
        self,
        historical_data: List[float],
        forecast: List[float]
    ) -> float:
        """Generate optimistic (bull) case scenario."""
        # Calculate historical growth rate
        growth_rate = (historical_data[-1] / historical_data[0]) ** (1 / len(historical_data)) - 1
        
        # Bull case: higher growth
        bull_growth = growth_rate * 1.5
        
        return forecast[-1] * (1 + bull_growth)
    
    def _generate_bear_case(
        self,
        historical_data: List[float],
        forecast: List[float]
    ) -> float:
        """Generate pessimistic (bear) case scenario."""
        # Bear case: negative or lower growth
        growth_rate = (historical_data[-1] / historical_data[0]) ** (1 / len(historical_data)) - 1
        bear_growth = growth_rate * 0.5
        
        return forecast[-1] * (1 + bear_growth)
    
    def _calculate_scenario_probabilities(
        self,
        historical_data: List[float],
        base: float,
        bull: float,
        bear: float
    ) -> Dict[str, float]:
        """Calculate probabilities for each scenario."""
        # Placeholder: Use historical volatility and distribution
        # Simple assumption for now
        return {
            'bull': 0.25,
            'base': 0.60,
            'bear': 0.15
        }
    
    def _assess_model_accuracy(
        self,
        historical_data: List[float],
        model: ForecastModel
    ) -> float:
        """Assess model accuracy using historical data."""
        # Placeholder: Use backtesting to assess accuracy
        # Return accuracy score between 0 and 1
        return 0.85
    
    def _apply_scenario_params(
        self,
        data: List[float],
        params: Dict[str, Any]
    ) -> List[float]:
        """Apply scenario parameters to data."""
        adjusted = data.copy()
        
        # Apply growth rate adjustment
        if 'growth_adjustment' in params:
            adjustment = params['growth_adjustment']
            adjusted = [v * (1 + adjustment) for v in adjusted]
        
        # Apply shock/event
        if 'shock' in params:
            shock = params['shock']
            adjusted = [v * (1 + shock) for v in adjusted]
        
        return adjusted


# Example usage
if __name__ == "__main__":
    agent = ForecastingAgent()
    
    # Sample historical data (TVL in billions)
    historical_tvl = [30, 32, 35, 38, 37, 39, 40]
    
    # Generate forecast
    forecast = agent.forecast(
        metric="Ethereum TVL",
        historical_data=historical_tvl,
        periods=30
    )
    
    print(f"Forecast for {forecast.metric}:")
    print(f"  Base case: ${forecast.base_case:.2f}B")
    print(f"  Bull case: ${forecast.bull_case:.2f}B (probability: {forecast.scenario_probabilities['bull']:.0%})")
    print(f"  Bear case: ${forecast.bear_case:.2f}B (probability: {forecast.scenario_probabilities['bear']:.0%})")
    print(f"  Model accuracy: {forecast.accuracy_score:.1%}")
