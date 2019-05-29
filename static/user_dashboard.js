"use strict";
function showDoctorInfo(results) {
    console.log(results, "Outside");
    let fn = results.fn;
    console.log(fn);

    var doctor_background_info = `<b>Doctor Name</b>: ${results.first_name} ${results.last_name} <br> 
                                <b>Address</b>: ${results.main_address} <br>
                                <b>Zipcode</b>: ${results.zipcode} <br>
                                <b>Speciality</b>: ${results.speciality_name} <br>
                                <b>NPI</b>: ${results.npi_id} <br>
                                <b>Doctor ID</b>: ${results.doctor_id}`;

    var doctor_hospital_info = 'doctor associated hospitals go here!!';

    var doctor_reviews_info = 'review info goes here!';

    // TODO: possibly consider using .empty().append() instead of .html() due to .html does not result in event firing
    $("#doctor-background-info").html(()=>{
        console.log(fn, "Inside displaying background info");
        if (results.first_name == undefined){
            console.log("Undefined doctor")
            return 'The doctor searched was not found. Please try again.';
        }else{
            console.log("Defined doctor", results.first_name)
            return doctor_background_info;
        }
    });

    $('#doctor-associated-hospital-info').html(()=>{
        console.log(fn, "Inside displaying hospital info");
         if (results.first_name == undefined){
            console.log("Undefined doctor")
            return '';
        }else{
            console.log("Defined doctor", results.first_name)
        
        return doctor_hospital_info;
        }
    });

    $('#doctor-reviews-info').html(()=>{
        console.log(fn, "Inside displaying reviews info");
        if (results.first_name == undefined){
            console.log("Undefined doctor")
            return '';
        }else{
            console.log("Defined doctor", results.first_name)
        
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

    let url = "/reviews"; //grab info from database
    console.log(url);
    // debugger;
    //Pull appropriate information about the doctor from the database
    $.get(url, formDoctor, showDoctorInfo);
    //Display information on dashboard
}

$("#reviews").on('submit', displayDoctor);