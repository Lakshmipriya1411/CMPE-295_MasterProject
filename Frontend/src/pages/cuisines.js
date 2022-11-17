import React, {Component} from 'react';
import {Link} from 'react-router-dom';

export default class Cuisines extends Component {

    constructor(props) {
        super(props)
        this.state = {
            cuisines: [
                {name: 'american', image: "https://x.yummlystatic.com/web/bubble/cuisine/american.png"},
                {name: 'african', image: "https://x.yummlystatic.com/web/bubble/cuisine/italian.png"},
                {name: 'italian', image: "https://x.yummlystatic.com/web/bubble/cuisine/italian.png"},
                {name: 'ianadian', image: "https://x.yummlystatic.com/web/bubble/cuisine/southern.png"},
                {name: 'european', image: "https://x.yummlystatic.com/web/bubble/cuisine/spanish.png"},
                {name: 'mexican', image: "https://x.yummlystatic.com/web/bubble/cuisine/mexican.png"},
                {name: 'thai', image: "https://x.yummlystatic.com/web/bubble/cuisine/thai.png"},
                {name: 'chinese', image: "https://x.yummlystatic.com/web/bubble/cuisine/chinese.png"},
                {name: 'indian', image: "https://x.yummlystatic.com/web/bubble/cuisine/indian.png"},
                {name: 'french', image: "https://x.yummlystatic.com/web/bubble/cuisine/french.png"},
                {name: 'greek', image: "https://x.yummlystatic.com/web/bubble/cuisine/greek.png"}
            ],
            isLoading: true
        };
    }

    handleViewCuisine = (value) => {
        console.log(value);
        localStorage.setItem("cuisineDetilsName", value.name);
    }

    render() {
        return (
            <div className="content-wrapper">
                <div className="content-header">
                    <div className="pantry-recipe-grid RecipeGrid">
                        <section className="pantry-grid-header">
                            <h4 className="grid-title h4-text primary-dark font-bold">Cuisines</h4>
                        </section>
                        <div className="row">
                            {this.state.cuisines.map((cuisine, index) =>
                                <Link className="col-md-3 pd-b" key={`${index}-il`} href="#" onClick={() => this.handleViewCuisine(cuisine)} to={`/cuisine-details`}>
                                    <img className="cuisine-image" src={cuisine.image} alt={cuisine.name}/>
                                    <div className="centered">{cuisine.name}</div>
                                </Link>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}