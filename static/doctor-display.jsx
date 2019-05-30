"use strict";

//Use event listener to use display provider info
/* class start */
class Reviews extends React.Component {
    constructor(props) {
        super(props);

        this.state = {reviews: []};


        // this.handleGuess = this.handleGuess.bind(this);
        //Make sure to bind all methods that update state
        this.updateReviews = this.updateReviews.bind(this);
}
    updateReviews(reviews){
        // update state
        return this.setState({reviews: reviews});
    }

    componentDidMount() {
        var that = this;
        console.log("In Component Mount lifecycle method!");
        fetch('/reviews')
            .then(res => {
                console.log(res);
                return res.json();
            })
            // .then(reviews_list => {debugger; this.setState({reviews:reviews_list}) ));
            .then(function(resp){
                that.updateReviews(resp.reviews);
                
            });

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
        let reviews = this.state.reviews.map(review => {
                    return <h1> {review} </h1>});
        return (
            <div>
                Reviews 
                <ol> 
                    <li>{reviews}</li>
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

