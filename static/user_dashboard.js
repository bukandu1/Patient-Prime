"use strict";


//$("user-favorite-doctors-list").html($.get("/update-favorite-doctors", results, )results.user_favorite_doctors);

function showDoctorInfo(results) {
    console.log(results, "Outside");
    console.log(results.first_name);

    //Format doctor's background information
    var doctor_background_info = `<b>Doctor Name</b>: ${results.first_name} ${results.last_name} <br> 
                                <b>Address</b>: ${results.main_address} <br>
                                <b>Zipcode</b>: ${results.zipcode} <br>
                                <b>Speciality</b>: ${results.speciality_name} <br>
                                <b>NPI</b>: ${results.npi_id} <br>
                                <b>Doctor ID</b>: ${results.doctor_id}`;

    //Format doctor's associated hospital information
    var doctor_hospital_info = results.associated_hospitals_list.map((hospital)=> {return `<button id = "${hospital}"> ${hospital}</button>`;});

    //Format doctor's review list
    var doctor_reviews_info = "<b>Reviews (10 Most Recent)</b>:<br>";

    // TODO: possibly consider using .empty().append() instead of .html() due to .html does not result in event firing
    //Display doctor's background information
    $("#doctor-background-info").html(()=>{
        console.log(results.first_name, "Inside displaying background info");
        if (results.first_name == undefined){
            console.log("Undefined doctor")
            return 'The doctor searched was not found. Please try again.';
        }else{
            console.log("Defined doctor", results.first_name)
            return '<div class="fb-share-button" data-href="https://google.com" data-layout="box_count" data-size="small"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgoogle.com%2F&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">Share</a></div>' + doctor_background_info;
        }
    });

    //Display doctor's associated hospitals
    $('#doctor-associated-hospital-info').html(()=>{
        console.log(results.first_name, "Inside displaying hospital info");
         if (results.first_name == undefined){
            console.log("Undefined doctor")
            return '';
        }else{
            console.log("Defined doctor", results.first_name)
        
        return 'Select One or more associated hospitals to view more information<br>' + doctor_hospital_info;
        }
    });

    //Display doctor's review list
    $('#doctor-reviews-info').html(()=>{
        console.log(results.first_name, "Inside displaying reviews info");


        if (results.first_name == undefined){
            console.log("Undefined doctor")
            return '';
        }else{
            console.log("Defined doctor", results.first_name)
            for (let review of results.reviews){
                doctor_reviews_info += `<div class="flex-item">${review}</div>`;
    }
        
        return doctor_reviews_info;
        }
    });

}

function displayDoctor(event) {
    event.preventDefault();
    console.log(event);


    //Retrieve the first and last name from the form
    let formDoctor = {"firstName": $("#doctor_first_name").val(), "lastName": $("#doctor_last_name").val()};
    console.log(formDoctor);

    let url = "/search-doctor"; //grab info from database
    console.log(url);
    //Pull appropriate information about the doctor from the database
    $.get(url, formDoctor, showDoctorInfo);
    //Display information on dashboard
}

$("#reviews").on('submit', displayDoctor);

function displayUpdatedFavorites(results){
    console.log("In the display updated favorites function")
    console.log(results.user_favorite_doctors);
    return $('#user-favorite-doctors-list').html(results.user_favorite_doctors.map((docs)=> {return `<ul><li>${docs}</li></ul>`;
        }));

}


function updateFavoriteDoctors(event){
    event.preventDefault();
    console.log(event);

    //let favoriteDoctor = {"firstName": $("#doctor_first_name").val(), "lastName": $("#doctor_last_name").val()};
    let url = "/update-favorite-doctors";

    $.get(url, displayUpdatedFavorites);
}

$("#button-favorite-current-doctor").on('click', updateFavoriteDoctors);

function displayHospitalChart(event){
    event.preventDefault();
    console.log("inside display hospital fx", event);
}
$(document).ready(function() {
    $("#test chart button").on('click', (event)=>{
    event.preventDefault();
    console.log("inside display hospital fx", event);
});
});

// TODO: Loop through associated hospital results
$("#UNIVERSITY OF MARYLAND MEDICAL CENTER").on('click', (event) => {
    console.log("inside display hospital ARROW function", event);
});

$("#JOHNS HOPKINS HOSPITAL, THE").on('click', displayHospitalChart);

// TODO: Delete hard-coded information once jQuery code works and AJAX setup
var associated_hospitals_list_measure_data = {"hospital_1": [{'x': 10, 'y':1, 'r':20}, {'x': 20, 'y':.5, 'r':30}], "hospital_2": [None]}
    


