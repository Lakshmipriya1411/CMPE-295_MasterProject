import React, {Component} from 'react';
import axios from "axios";
import {Link} from 'react-router-dom';
import Rating from "react-rating";
import searchRes from './../search.jpg';

export default class Home extends Component {
    constructor(props) {
        super(props)
        this.state = {
            email: '',
            password: '',
            redirect: false,
            authError: false,
            isLoading: false,
            ingredients: [],
            selectedIngredient: [],
            searchKeyResult: [],
            ingredientsOrg: [],
            searchRecipe: [],
            search: false,
        };
    }


    handleSearch = () => {
        this.setState({isLoading: true});
        const url = 'http://127.0.0.1:5000/api/recipes/ingredients';

        const payload = {ingredients: this.state.selectedIngredient}
        axios.post(url, payload)
            .then(result => {
                const data = result.data;
                this.setState({searchRecipe: data.recipes.slice(0, 8), search: true, isLoading: false}, () => {});
            })
            .catch(error => {
                console.log(error);
                this.setState({authError: true, isLoading: false});
            });
    };

    componentDidMount() {
        const url = 'http://127.0.0.1:5000/api/ingredients';
        axios.get(url)
            .then(response => {
                const ingredients = response.data;
                this.setState({ingredients: ingredients.ingredients.slice(0, 20), ingredientsOrg: ingredients.ingredients});
            })
            .catch(error => {
                this.setState({toDashboard: true});
                console.log(error);
            });
    }

    handleAddIngredient = (value) => {
        const index = this.state.ingredients.indexOf(value)
        if (index !== -1) {
            this.state.ingredients.splice(index, 1);
            this.setState({ingredients: this.state.ingredients});
        }
        this.setState({selectedIngredient: [...this.state.selectedIngredient, value]});
    }

    handleViewRecipe = (value) => {
        console.log(value);
        localStorage.setItem("detilsId", value.id);
    }

    handleRemoveIngredient = (value) => {
        const index = this.state.selectedIngredient.indexOf(value)
        if (index !== -1) {
            this.state.selectedIngredient.splice(index, 1);
            this.setState({ingredients: this.state.selectedIngredient});
        }
        this.setState({ingredients: [...this.state.ingredients, value]})
    }

    handleLoginKeyUp = (e) => {
        const temp = [];
        if (e.target.value.length > 1) {
            this.state.ingredientsOrg.map((a) => {
                console.log(a.substr(0, e.target.value.length).toLowerCase() === e.target.value.toLowerCase())
                if (a.includes(e.target.value.toLowerCase()) && (a.substr(0, e.target.value.length).toLowerCase() === e.target.value.toLowerCase())) {
                    temp.push(a)
                    console.log(a.substr(0, e.target.value.length).toLowerCase())
                }
            });
            this.setState({searchKeyResult: temp.slice(0, 5)});
        }
        console.log(this.state.searchKeyResult)
    }


    render() {
        const isLoading = this.state.isLoading;
        return (
            <div className="content-wrapper">
                <div className="content-header bakimage">
                    <section className="content">
                        <div className="container-fluid">
                            {/*<h2 className="text-center display-4">Search</h2>*/}
                            <div className="flot20">
                                <div className="col-md-12 pantry-ingredient-search">
                                    <form className="suggest-form desktop pantry-search">
                                        <div role="combobox" aria-haspopup="listbox" aria-owns="react-autowhatever-1" aria-expanded="false" className="ingredient-suggest-container">
                                            <input type="text" autoComplete="off" aria-autocomplete="list" aria-controls="react-autowhatever-1" className="ingredient-suggest-input p1-text" name="IngredientSuggestInput" onKeyUp={(e) => this.handleLoginKeyUp(e)} placeholder="Enter your ingredients"/>
                                            <div id="react-autowhatever-1" role="listbox" className="suggestion-container">
                                                <div className="search-bubbles-section">
                                                    <div className="pantry-suggest-tooltip micro-text font-normal"/>
                                                    {/*<p className="micro-caps font-bold search-bubble-title greyscale-3">Suggested Ingredients</p>*/}
                                                    <div className="search-bubbles has-gradient" id="pantry-suggested-ingredients">
                                                        {this.state.ingredients.map((ingredient, index) =>
                                                            <div key={`${index}key`} className="suggested-ingredient floating button" data-name={ingredient} onClick={() => this.handleAddIngredient(ingredient)}>
                                                                <span className="ingredient-content">
                                                                    <span className="ingredient-name">{ingredient}</span>
                                                                </span>
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                            <div id="react-autowhatever-2" role="listbox" className="suggestion-containe hidden">
                                                <ul role="listbox">
                                                    {this.state.searchKeyResult.map((search, index) =>
                                                        <li key={`key${index}`} role="option" id={`react-autowhatever-1--item${index}`} aria-selected="false" onClick={() => this.handleAddIngredient(search)} className="ingredient-suggestion" data-suggestion-index="3">
                                                            <div className="ingredient-suggest-item p2-text">
                                                                <span className="suggestion-text ml29">{search}</span>
                                                                <i className="fa fa-plus-circle font search-plus" aria-hidden="true"></i>
                                                            </div>
                                                        </li>
                                                    )}
                                                </ul>
                                            </div>
                                        </div>
                                        <i className="fa fa-plus-circle" aria-hidden="true"/>
                                        <i className="fa fa-times-circle" aria-hidden="true"/>
                                    </form>
                                </div>
                                <h4 className="micro-caps font-bold search-bubble-title greyscale-3">Your Kitchen Ingredients</h4>
                                <div className="pantry-ingredient-list-wrapper">
                                    <div className="pantry-ingredient-list">
                                        {this.state.selectedIngredient.map((ingredient, index) =>
                                            <div className="button suggested-ingredient floating" key={`${index}slected`}>
                                                <div className="ingredient-content">
                                                    <span className="ingredient-name">{ingredient}</span>
                                                    <i className="fa fa-times" aria-hidden="true" onClick={() => this.handleRemoveIngredient(ingredient)}/>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                                <div className="submit-search">
                                    <button title="Search Recipes" aria-label="Search Recipes" className="button search-submit-button btn-primary" onClick={() => this.handleSearch()}>
                                        {isLoading ? (
                                            <span className="ptlr spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                        ) : (
                                            <span>Search Recipes</span>
                                        )}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </section>

                    {this.state.search ? (
                        <div className="pantry-recipe-grid RecipeGrid ">
                            <section className="pantry-grid-header">
                                <h4 className="grid-title h4-text primary-dark font-bold">Recipes that match your Ingredients</h4>
                            </section>
                            <section className="flex-row card-list">
                                {this.state.searchRecipe.map((recipe, index) =>
                                    <div key={`${index}-key`} className="recipe-card ingredients-hover single-recipe visible GuidedRecipe YummlyOriginal" data-url="5-Ingredient-Sugar-Cookies-2376884" role="link" id="05-Ingredient-Sugar-Cookies-2376884">
                                    {/*<span className="paywall-action-text justification-flag font-bold background-light micro-text">*/}
                                    {/*<span className="icon locked  y-icon" data-icon=""></span>*/}
                                    {/*<span className="text ">Original</span></span>*/}
                                        <div className="recipe-card-img-wrapper">
                                            <div>
                                                {recipe.image ? (
                                                    <img src={recipe.image} style={{height: '217px'}} alt={recipe.title}/>
                                                ) : (
                                                    <div>
                                                        <img alt={recipe.title} src={searchRes} className="recipe-card-img placeholder" width="220" height="220"/>
                                                        <img alt={recipe.title} src={searchRes} className="recipe-card-img full" width="220" height="220"/>
                                                    </div>
                                                )}
                                            </div>

                                            <a className="card-ingredients font-light micro-text flex-column" tabIndex="-1" title="5-Ingredient Sugar Cookies" aria-label="5-Ingredient Sugar Cookies" href="#">
                                                <span title="baking soda, granulated sugar, salted butter, all-purpose flour, large eggs, granulated sugar">baking soda, granulated sugar, salted butter, all-purpose flour and 2 more</span></a></div>
                                        <Link className="link-overlay" tabIndex="-1" title={recipe.title} aria-label={recipe.title} onClick={() => this.handleViewRecipe(recipe)} to={`/recipe-details`}></Link>
                                        <div className="card-info-wrapper flex-row">
                                            <div className="card-info primary-dark">
                                                <a className="card-title two-line-truncate p2-text font-normal" title={recipe.title} aria-label={recipe.title} href="#">{recipe.title}</a>
                                                <a className="review-stars micro-text" tabIndex="-1" title="Rated 4.17 Out of 5 by Yummly Users" aria-label="Rated 4.17 Out of 5 by Yummly Users" href="#">
                                                    <Rating
                                                        readonly
                                                        placeholderRating={recipe.rating}
                                                        emptySymbol={<img src="http://dreyescat.github.io/react-rating/assets/images/star-grey.png" className="icon"/>}
                                                        placeholderSymbol={<img src="http://dreyescat.github.io/react-rating/assets/images/star-red.png" className="icon"/>}
                                                        fullSymbol={<img src="http://dreyescat.github.io/react-rating/assets/images/star-yellow.png" className="icon"/>}
                                                    />
                                                </a>
                                            </div>
                                            <div className="card-action no-padding type-add primary-teal">
                                                <i className="fa fa-plus-circle font" aria-hidden="true"></i>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </section>
                            <section className="spinner-section">
                                <div className="spinner light"><img alt="" src="https://x.yummlystatic.com/web/1x1.png" loading="lazy" width="200" height="200"/></div>
                            </section>
                        </div>
                    ) : (
                        <span></span>
                    )
                    }
                </div>
            </div>

        )
    }
}