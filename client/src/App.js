import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HoroscopePrediction from './pages/HoroscopePrediction';

function App() {
    return (
        <Router>
            <Switch>
                <Route path="/horoscope-prediction" component={HoroscopePrediction} />
                {/* Các route khác */}
            </Switch>
        </Router>
    );
}

export default App;
