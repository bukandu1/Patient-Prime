
"use strict";


//$("user-favorite-doctors-list").html($.get("/update-favorite-doctors", results, )results.user_favorite_doctors);

function showDoctorInfo(results) {
    console.log(results, "Outside");
    console.log(results.first_name);
    console.log(results.associated_hospitals_list);

    //Format doctor's background information
    var doctor_background_info = `<b>Doctor Name</b>: ${results.first_name} ${results.last_name} <br> 
                                <b>Address</b>: ${results.main_address} <br>
                                <b>Zipcode</b>: ${results.zipcode} <br>
                                <b>Speciality</b>: ${results.speciality_name} <br>
                                <b>NPI</b>: ${results.npi_id} <br>
                                <b>Doctor ID</b>: ${results.doctor_id}`;

    //Format doctor's associated hospital information
    var doctor_hospital_info = results.associated_hospitals_list.map((hospital)=> 
        {return `<button class="hospital_button" id="${hospital.hospital_id}"value ="${hospital.name}"> 
                    ${hospital.name}</button>`;});

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
            return doctor_background_info + 
            '<div class="fb-share-button" data-href="https://google.com" data-layout="box_count" data-size="small"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgoogle.com%2F&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">Share</a></div>' 
            ;
        }
    });

    //Display doctor's associated hospitals
    $('#two').html(()=>{
        console.log(results.first_name, "Inside displaying hospital infozzzzzz");
         if (results.first_name == undefined){
            console.log("Undefined doctor")
            return '';
        }else{
            console.log("Defined doctor", results.first_name)
        
        return 'Select One or more associated hospitals to view more information<br>' 
        + doctor_hospital_info + `<canvas id="myChart" width="400" height="400"></canvas>`;
        }
    });

    //Display doctor's review list
    $('#doctor-reviews-info').html(()=>{
        console.log(results.first_name, "Inside displaying reviews info");


        if (results.first_name == undefined || results.last_name == undefined){
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
        //event.preventDefault();
        console.log("inside display hospital fx", event);
    }


$("#testchartbutton").on('click', (event)=>{
    event.preventDefault();
    console.log("inside display hospital fx", event);
});

    // TODO: Loop through associated hospital results
$("#two").on('click', "button", (event) => {
    console.log("inside display hospital ARROW function", event);
    console.log(event.currentTarget.id);

    // $('#myChart').empty();
    var ctx = document.getElementById("myChart").getContext('2d');
  // ajax

    // var myChart = new Chart(ctx, config);
var forecast_chart = new Chart(ctx, config);
$(`#${event.currentTarget.id}`).click(function() {
    console.log(`Going to grab ${event.currentTarget.id}'s information!`);
    var data = forecast_chart.config.data;
    data.datasets[0].data = temp_dataset;
    //data.datasets[0].data = rain_dataset;
    data.labels = chart_labels;
    forecast_chart.update();
});

});

// TODO: Delete hard-coded information once jQuery code works and AJAX setup
var more_test_data = {"hospital_1": [{'x': 10, 'y':1, 'r':20}, {'x': 20, 'y':.5, 'r':30}], "hospital_2": [null]}
var hospital_1 = more_test_data.hospital_1 //list of 
console.log(hospital_1);

// $("#myChart").html(`
//   var ctx = document.getElementById('myChart');
//   var myChart = new Chart(ctx, {
//       "type":"bubble",
//       "data":{
//           "datasets":[{
//               "label":"First Dataset",
//               "data":[{
//                   "x":20,"y":30,"r":15},
//                   {"x":40,"y":10,"r":10},{'x': 10, 'y':1, 'r':20}, {'x': 20, 'y':.5, 'r':30}
//                   ],
//               "backgroundColor":"rgb(255, 99, 132)"
//             }]}});
// ")`);

var chart_labels = ['06:00', '09:00', '12:00', '15:00', '18:00', '21:00'];
var temp_dataset = [{
                  "x":20,"y":30,"r":15},
                  {"x":40,"y":10,"r":10},{'x': 10, 'y':1, 'r':20}, {'x': 30, 'y':.5, 'r':30},
                  {'x': 50, 'y':.5, 'r':30}
                  ];
var rain_dataset = [{
                  "x":20,"y":30,"r":40},
                  {"x":40,"y":10,"r":10},{'x': 20, 'y':5, 'r':20}, {'x': 30, 'y':.5, 'r':30},
                  {'x': 50, 'y':.5, 'r':30}
                  ];
var ctx = document.getElementById("myChart").getContext('2d');
var config = {
      "type":"bubble",
      "data":{
          "labels": chart_labels,
          "datasets":[{
              "label":"Patient Safety Indicators",
              "data":[{
                  "x":20,"y":30,"r":15},
                  {"x":40,"y":10,"r":10},{'x': 10, 'y':1, 'r':20}, {'x': 30, 'y':.5, 'r':30},
                  {'x': 45, 'y':.5, 'r':30}
                  ],
              "backgroundColor":"rgb(255, 99, 132)"
            }]}};


var myChart = new Chart(ctx, {
      "type":"bubble",
      "data":{
          "labels": chart_labels,
          "datasets":[{
              "label":"First Dataset",
              "data":[{
                  "x":20,"y":30,"r":15},
                  {"x":40,"y":10,"r":10},{'x': 10, 'y':1, 'r':20}, {'x': 30, 'y':.5, 'r':30},
                  {'x': 50, 'y':.5, 'r':30}
                  ],
              "backgroundColor":"rgb(255, 99, 132)"
            }]}});
var forecast_chart = new Chart(ctx, config);

$("#19").click(function() {
    // var chart_labels = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'];
    // var temp_dataset = ['5', '3', '4', '8', '10', '11', '10', '9'];
    var rain_dataset = ['0', '0', '1', '4', '19', '19', '7', '2'];
    var data = forecast_chart.config.data;
    data.datasets[0].data = temp_dataset;
    data.datasets[1].data = rain_dataset;
    data.labels = chart_labels;
    forecast_chart.update();
});





// {
//     type: 'bar',
//     data: {
//         labels: chart_labels,
//         datasets: [{
//             type: 'line',
//             label: "Temperature (Celsius)",
//             yAxisID: "y-axis-0",
//             fill: false,
//             data: temp_dataset,
//         }, {
//             type: 'bar',
//             label: "Precipitation (%)",
//             yAxisID: "y-axis-1",
//             data: rain_dataset,
//         }]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 position: "left",
//                 "id": "y-axis-0",
//             }, {
//                 position: "right",
//                 "id": "y-axis-1",
//             }]
//         }
//     }
// };





