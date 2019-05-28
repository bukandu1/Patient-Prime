"use strict";

//Use event listener to use display provider info
/* class start */
class Reviews extends React.Component {
    constructor() {
        super();

        this.state = {reviews: [""]};
}

    componentDidMount() {

        console.log("In Component Mount lifecycle method!");
        fetch('/reviews')
            .then(res => {
                console.log(res);
                return res.json();
            })
            .then(reviews_list => this.setState({reviews:reviews_list}));
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
        debugger;
        const { reviews } = this.state;
        const reviewsList  = this.state.reviews.reviews;
        console.log(reviewsList);
        return (
            <div>
                Reviews 
                <ol> 
                    <li>{this.state.reviews.reviews}</li>
                </ol>
                <ul>
                    <li>test1</li>
                </ul>
            </div>
                )
 
            }
}
  
    
//end Review class

ReactDOM.render(
    <Reviews />,
    document.getElementById('root')
);

