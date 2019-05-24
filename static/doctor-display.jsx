"use strict";

//Use event listener to use display provider info
/* class start */
class Reviews extends React.Component {
    constructor() {
        super();

        // Should this just be a list of reviews
        this.state = { reviews : []
    };
}

    componentDidMount() {

        console.log("In Component Mount lifecycle method!");
        fetch('/reviews')
            .then(res => res.json())
            .then(reviews_list => {
                this.setState({reviews:reviews_list});
            });
    }

    
    // reviewDisplay = (review) => {
    //     console.log("In reviewDisplay function")
    //     console.log(review)
    // }

    render() {
        return (
            <div>
                <h1>Reviews</h1> 
                {
                    this.state.reviews.map(review=> {
                        return {review};
                    }
                    )
                }
            </div>
        );
    }
 
}//end Review class

ReactDOM.render(
    <Reviews />,
    document.getElementById('root')
);

