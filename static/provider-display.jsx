"use strict";

//Use event listener to use display provider info
/* class start */
class Hospital extends React.Component {
    constructor() {
        super();

        this.state = { value: '?' };  // Set initial value 
    }

    render() {
        return (
            <div>
                <h1>Testing DIV</h1>
            </div>
        );
    }
 
}

ReactDOM.render(
    <Hospital />,
    document.getElementById('root')
);