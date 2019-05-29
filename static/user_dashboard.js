"use strict";
function updateDoctor(results) {
    console.log(results, "Outside");
    let fn = results.fn;
    console.log(fn);
    $("#search-doctor-display").html(()=>{
        console.log(fn, "Inside");
        return "First Name: "  + results.fn + "Last Name: " + results.ln;
    });
}
// `${}`
        
        


function displayDoctor(event) {
    event.preventDefault();
    console.log(event);


    //Retrieve the first and last name from the form
    let formDoctor = {"firstName": $("#doctor_first_name").val(), "lastName": $("#doctor_last_name").val()};
    console.log(formDoctor);

    let url = "/reviews"; //grab info from database
    console.log(url);
    // debugger;
    //Pull appropriate information about the doctor from the database
    $.get(url, formDoctor, updateDoctor);
    //Display information on dashboard
}

$("#reviews").on('submit', displayDoctor);