import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from "./pages/home";
import Header from "./elements/header";
import Sidebar from "./elements/sidebar";
import React from "react";
import Footer from "./elements/footer";
import NonVegRecipes from "./pages/non-veg-recipes";
import Cuisines from "./pages/cuisines";
import VegRecipes from "./pages/veg-recipes";
import TopRecomended from "./pages/top-recomended";
import Login from "./pages/login";
import Register from "./pages/register";
import RecipeDetails from "./pages/recipe-details";
import CuisineDetails from "./pages/cuisine-details";

function App() {
    return (
        <div className="App">
            <div className="wrapper">
                <Router>
                    {window.location.pathname !== '/login' && window.location.pathname !=='/register' && <Sidebar/>}
                    <Routes>
                        <Route exact path="/" element={<Home/>}/>
                        <Route path="home" element={<Home/>}/>
                        <Route path="top-recomended" element={<TopRecomended/>}/>
                        <Route path="veg-recipes" element={<VegRecipes/>}/>
                        <Route path="non-veg-recipes" element={<NonVegRecipes/>}/>
                        <Route path="cuisines" element={<Cuisines/>}/>
                        <Route path="login" element={<Login/>}/>
                        <Route path="register" element={<Register/>}/>
                        <Route path="recipe-details" element={<RecipeDetails/>}/>
                        <Route path="cuisine-details" element={<CuisineDetails/>}/>
                    </Routes>
                    {window.location.pathname !== '/login' && window.location.pathname !=='/register' && <Footer/>}
                </Router>
            </div>
        </div>
    );
}

export default App;
