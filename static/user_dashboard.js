"use strict";


//$("user-favorite-doctors-list").html($.get("/update-favorite-doctors", results, )results.user_favorite_doctors);

function showDoctorInfo(results) {
    console.log(results, "Outside");
    console.log(results.first_name);
    console.log(results.associated_hospitals_list);

    //Format doctor's background information
    var doctor_background_info = `<p><b><h1>${results.first_name} ${results.last_name} </b></h1></p> 
                                <p><b>Address</b>: ${results.main_address} <br></p>
                                <p><b>Zipcode</b>: ${results.zipcode} <br></p>
                                <p><b>NPI</b>: ${results.npi_id} <br></p>
                                <p><b>Doctor ID</b>: ${results.doctor_id}</p>
                                <p><b>Speciality</b>: <span class="tags">${results.speciality_name} </span><br></p>
                                <div class="col-xs-12 divider text-center">
                
                <div class="col-xs-12 emphasis">
                    <h2><strong>Text This Doctor to a Friend</strong></h2>                    
                    <button class="btn btn-info btn-block"><span class="fa fa-user"></span> Share (Messaging & Data Rates Apply) </button>
                    
                  </div>
                <p>
                </div>
                `;

    //Format doctor's associated hospital information
    var doctor_hospital_info = results.associated_hospitals_list.map((hospital)=> {
        return `
          <li>
            <button class="clean center" id=${hospital.hospital_id} value=${hospital.name}>
              ${hospital.name}
            </button>
          </li>
        `;
    }).join('');
        
          // return `<li><button class="hospital_button clean center" id="${hospital.hospital_id}"value ="${hospital.name}"> 
          //           ${hospital.name}</button></li>`;});

    //Format doctor's review list
    var doctor_reviews_info = "<small>(10 Most Recent)</small>:<br>";

    // TODO: possibly consider using .empty().append() instead of .html() due to .html does not result in event firing
    //Display doctor's background information
    $(".doctor-background-info").html(()=>{
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
    $('.two').html(()=>{
        console.log(results.first_name, "Inside displaying hospital infozzzzzz");
         if (results.first_name == undefined){
            console.log("Undefined doctor")
            return '';
        }else{
            console.log("Defined doctor", results.first_name)
        
        return '<h1>Associated Hospitals</h1><br> Select an associated hospitals to view more information' 
        + doctor_hospital_info + `<canvas id="myChart" width="300" height="250"></canvas>`;
        }
    });

    //Display doctor's review list
    $('.doctor-reviews-info').html(()=>{
        console.log(results.first_name, "Inside displaying reviews info");

        // TODO: Fix log. Currently error if last name not in system
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
    // TODO: Update class names with dashes (-)
    let $form = $(event.target) //jQuery object --> form 
    let formDoctor = {"firstName": $form.find(".doctor_first_name").val(), 
                      "lastName": $form.find(".doctor_last_name").val()};
    console.log($form.find(".doctor_first_name").val());
    console.log(formDoctor);

    let url = "/search-doctor"; //grab info from database
    console.log(url);
    //Pull appropriate information about the doctor from the database
    $.get(url, formDoctor, showDoctorInfo);
    //Display information on dashboard
}

$(".reviews").on('submit', displayDoctor);

// TODO: Add conditional for when there are no favorites to be shown
function displayUpdatedFavorites(results){
    console.log("In the display updated favorites function")
    console.log(results.user_favorite_doctors);
    return $('.user-favorite-doctors-list').html(results.user_favorite_doctors.map((docs)=> {return `<li>${docs}</li><br>`;
        }));

}


function updateFavoriteDoctors(event){
    event.preventDefault();
    console.log(event);

    //let favoriteDoctor = {"firstName": $("#doctor_first_name").val(), "lastName": $("#doctor_last_name").val()};
    let url = "/update-favorite-doctors";

    $.get(url, displayUpdatedFavorites);
}

$(".button-favorite-current-doctor").on('click', updateFavoriteDoctors);

// TODO: Fix toggle to check if already favorited. Bug fix.
$(".button-favorite-current-doctor").click(function(){

        $(this).text($(this).text() == 'Favorite The Doctor Above!' ? 'Unfavorite The Doctor Above' : 'Favorite The Doctor Above!');
    });


function displayHospitalChart(event){
        //event.preventDefault();
        console.log("inside display hospital fx", event);
    }


    // TODO: Loop through associated hospital results
$(".two").on('click', "button", (event) => {
    console.log("inside display hospital ARROW function", event);
    console.log(event.currentTarget.id);

    // $('#myChart').empty();


    // TODO: Delete hard-coded information once jQuery code works and AJAX setup
    //var forecast_chart = new Chart(ctx, config);
    $('#3').on('click', (function(event) {
        //myChart.destroy();
        console.log(`Going to grab ${event.currentTarget.id}s information!`);
        var ctx = document.getElementById("myChart").getContext('2d');
        var config = {
          "type":"bubble",
          "data":{
              "datasets":[{
                  label: ["Serious (Preventable) Complications"],
                  backgroundColor: "rgba(60,186,159,1)",
                  //borderColor: "rgba(255,221,50,1)",
                  data: [{
                    x: 10,
                    y: 5.0,
                    r: 40
                  }]
                },{
                  label: ["Sepsis/Bloodstream Infection"],
                  backgroundColor: "rgba(255,221,50,1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 15,
                    y: 10,
                    r: 20
                  }]
                },{
                  label: ["Clots/DVT"],
                  backgroundColor: "rgb(255, 99, 132)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 20,
                    y: 5,
                    r: 20
                  }]
                },{
                  label: ["Ulcers"],
                  backgroundColor: "rgba(22, 96, 173, 1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 30,
                    y: 40,
                    r: 30
                  }]
                },{
                  label: ["Wound Opening/Dehiscence"],
                  backgroundColor: "rgba(193,46,12,1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 40,
                    y: 30,
                    r: 20
                  }]
                },{
                  label: ["Cut/Lacerations"],
                  backgroundColor: "rgba(186,24,62,1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 50,
                    y: .0,
                    r: 10
                  }]
                }]
      },
    options: {
      title: {
        display: true,
        text: 'Patient Safety Measures'
      }, 
      scales: {
        yAxes: [{ 
          scaleLabel: {
            display: true,
            labelString: "Patients per 1000"
          }
        }],
        xAxes: [{ 
          scaleLabel: {
            display: true,
            labelString: "Measures"
          }
        }]
      },
      legend: {
        display: true,
        position: 'bottom',
        labels:
        {
          fontColor: '#000080',
        }
      }
      }
  };
        var myChart = new Chart(ctx, config);
        console.log("3 was created");
        }));


    $('#19').on('click', (function(event) {
        //myChart.destroy();
        console.log(`Going to grab ${event.currentTarget.id}s information!`);
        var ctx = document.getElementById("myChart").getContext('2d');
        var config = {
          "type":"bubble",
          "data":{
              "datasets":[{
                  label: ["Serious (Preventable) Complications"],
                  backgroundColor: "rgba(60,186,159,1)",
                  //borderColor: "rgba(255,221,50,1)",
                  data: [{
                    x: 25,
                    y: 1,
                    r: 40
                  }]
                },{
                  label: ["Sepsis/Bloodstream Infection"],
                  backgroundColor: "rgba(255,221,50,1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 15,
                    y: 10,
                    r: 20
                  }]
                },{
                  label: ["Clots/DVT"],
                  backgroundColor: "rgb(255, 99, 132)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 5,
                    y: 5,
                    r: 20
                  }]
                },{
                  label: ["Ulcers"],
                  backgroundColor: "rgba(22, 96, 173, 1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 45,
                    y: 35,
                    r: 30
                  }]
                },{
                  label: ["Wound Opening/Dehiscence"],
                  backgroundColor: "rgba(193,46,12,1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 40,
                    y: 20,
                    r: 20
                  }]
                },{
                  label: ["Cut/Lacerations"],
                  backgroundColor: "rgba(186,24,62,1)",
                  //borderColor: "rgba(255,221,50,0.2)",
                  data: [{
                    x: 50,
                    y: 40,
                    r: 10
                  }]
                }]
      },
      options: {
      title: {
        display: true,
        text: 'Patient Safety Measures'
      }, 
      scales: {
        yAxes: [{ 
          scaleLabel: {
            display: true,
            labelString: "Patients per 1000"
          }
        }],
        xAxes: [{ 
          scaleLabel: {
            display: true,
            labelString: "Measures"
          }
        }]
      },
      legend: {
        display: true,
        position: 'bottom',
        labels:
        {
          fontColor: '#000080',
        }
      }
    }
    };

        var myChart = new Chart(ctx, config);
        }));
});

var more_test_data = {"hospital_1": [{'x': 10, 'y':1, 'r':20}, {'x': 20, 'y':.5, 'r':30}], "hospital_2": [null]}
var hospital_1 = more_test_data.hospital_1 //list of 
console.log(hospital_1);

var ctx = document.getElementById("myChart").getContext('2d');

var data = [
            {"x":20,"y":10,"r":15},
            {"x":40,"y":9,"r":10},
            {'x': 10, 'y':8, 'r':20}, 
            {'x': 30, 'y':7, 'r':30},
            {'x': 50, 'y':6, 'r':30},
            {'x': 20, 'y':5, 'r':30}

            ]

var data2 = [
            {"x":30,"y":10,"r":10},
            {"x":20,"y":9,"r":10},
            {'x': 50, 'y':8, 'r':10}, 
            {'x': 30, 'y':5, 'r':30},
            {'x': 40, 'y':5, 'r':20},
            {'x': 10, 'y':7, 'r':20}

            ]


// var myChart = new Chart(ctx, {
//       "type":"bubble",
//       "data":{
//           "labels": chart_labels,
//           "datasets":[{
//               "label":"First Dataset",
//               "data":[
//                   {"x":20,"y":30,"r":15},
//                   {"x":40,"y":10,"r":10},
//                   {'x': 10, 'y':1, 'r':20}, 
//                   {'x': 30, 'y':.5, 'r':30},
//                   {'x': 50, 'y':.5, 'r':30}
//                   ],
//               "backgroundColor":"rgb(255, 99, 132)"
//             }]}});
//var forecast_chart = new Chart(ctx, config);

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

// Log out functionality
$("logout").click(function(){
  url = "/logout";
  $.get(url, ()=> {
    alert("You have logged out. Come back again!");
  });
});