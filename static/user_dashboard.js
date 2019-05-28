"use strict";
function updateDoctor(results) {
    console.log(results, "Outside");
    $("#search-doctor-display").html(results)=> {
        console.log(results, "Inside");
        debugger;
        return "First Name: "  + results.fn + " Last Name: " + results.ln;
    });
}


function displayDoctor(event) {
    event.preventDefault();
    console.log(event);

    let url = "/reviews.json"; //grab info from database
    console.log(url);

    //Retrieve the first and last name from the form
    let formData = {"firstName": $("#doctor_first_name").val(), "lastName": $("#doctor_last_name").val()};
    console.log(formData);
    //Pull appropriate information about the doctor from the database
    $.get(url, formData, updateDoctor);
    //Display information on dashboard
}

$("#reviews").on('submit', displayDoctor);