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
            .then(res => {
                console.log(res);
                return res.json();
            })
            .then(reviews_list => this.setState({reviews: reviews_list}));
      //           // this.setState({todos: this.state.todos.map(todo=>{
      // if (todo.id === id){
      //   todo.completed = !todo.completed //toggles
      // }
      // return todo;
            }
    // reviewDisplay = (review) => {
    //     console.log("In reviewDisplay function")
    //     console.log(review)
    // }

    render() {
        const { reviews } = this.state

        return (
            <div>
            Reviews 
                    <ul> 
                        {this.state.reviews.reviews

                            // .map(review => 
                            // <li key = {review.review_id}>
                            // {reviews.review_text_body}
                            // </li>
                        }
                        </ul>
                    );
            
                    </div>
                )
 
            }
        }
//end Review class

ReactDOM.render(
    <Reviews />,
    document.getElementById('root')
);

