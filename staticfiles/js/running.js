var self_js_script = $('script[src*=running]'); // or better regexp to get the file name..

var analysis_code = self_js_script.attr('analysis_code');
var homepage_status = self_js_script.attr('homepage_status');
var YOUTH_json_file = self_js_script.attr('YOUTH_json_file');
var ADULT_json_file = self_js_script.attr('ADULT_json_file');
var ELDER_json_file = self_js_script.attr('ELDER_json_file');
// if (typeof my_var_1 === "undefined" ) {
//    var my_var_1 = 'some_default_value';
// }
// alert(analysis_code); // to view the variable value
// alert(homepage_status); // to view the variable value

function setChart(data, gp_idx, chart_id) {
  var ctx = document.getElementById("g"+gp_idx.toString()+"_"+chart_id);
  if (chart_id.includes("totalInfected")) {
    var backgroundColor = 'rgba(255, 99, 132, 0.2)';
    var borderColor = 'rgba(255,99,132,1)';
    var label = "Total Infected";
  } else if (chart_id.includes("currentInfected")) {
    var backgroundColor = 'rgba(255, 99, 132, 0.2)';
    var borderColor = 'rgba(255,99,132,1)';
    var label = "Current Infected";
  } else if (chart_id.includes("newInfected")) {
    var backgroundColor = 'rgba(255, 99, 132, 0.2)';
    var borderColor = 'rgba(255,99,132,1)';
    var label = "New Infected";
  } else if (chart_id.includes("totalSeekMed")) {
    var backgroundColor = 'rgba(190, 107, 207, 0.2)';
    var borderColor = 'rgba(190, 107, 207,1)';
    var label = "Total Medical Treatment";
  } else if (chart_id.includes("currentSeekMed")) {
    var backgroundColor = 'rgba(190, 107, 207, 0.2)';
    var borderColor = 'rgba(190, 107, 207,1)';
    var label = "Current Medical Treatment";
  } else if (chart_id.includes("newSeekMed")) {
    var backgroundColor = 'rgba(190, 107, 207, 0.2)';
    var borderColor = 'rgba(190, 107, 207,1)';
    var label = "New Medical Treatment";
  } else if (chart_id.includes("newDeath")) {
    var backgroundColor = 'rgba(54, 162, 235, 0.2)';
    var borderColor = 'rgba(54, 162, 235, 1)';
    var label = "New Death";
  } else if (chart_id.includes("totalDeath")) {
    var backgroundColor = 'rgba(54, 162, 235, 0.2)';
    var borderColor = 'rgba(54, 162, 235, 1)';
    var label = "Total Death";
  } else if (chart_id.includes("totalRecovery")) {
    var backgroundColor = 'rgba(255, 206, 86, 0.2)';
    var borderColor = 'rgba(255, 206, 86, 1)';
    var label = "Total Recovery";
  } else if (chart_id.includes("newRecovery")) {
    var backgroundColor = 'rgba(255, 206, 86, 0.2)';
    var borderColor = 'rgba(255, 206, 86, 1)';
    var label = "New Recovery";
  } else if (chart_id.includes("totalReachDay")) {
    var backgroundColor = 'rgba(75, 192, 192, 0.2)';
    var borderColor = 'rgba(75, 192, 192, 1)';
    var label = "Total Patients Reached Transmission Days";
  // } else if (chart_id.includes("newReachDay")) {
  //   var backgroundColor = 'rgba(75, 192, 192, 0.2)';
  //   var borderColor = 'rgba(75, 192, 192, 1)';
  //   var label = "New Patients Reached Transmission Days";
  // }
  } else if (chart_id.includes("cost_results")) {
    var backgroundColor = 'rgba(75, 192, 192, 0.2)';
    var borderColor = 'rgba(75, 192, 192, 1)';
    var label = "Cost of Each Subitem";
  }

  // console.log('data["Group_"+gp_idx.toString()]["labels"]: ', data["Group_"+gp_idx.toString()]["labels"])

  // console.log('[data["Group_"+gp_idx.toString()][chart_id+"_sz"]]: ', [data["Group_"+gp_idx.toString()][chart_id+"_sz"]])
  // console.log('data["Group_"+gp_idx.toString()][chart_id+"_sz"]: ', data["Group_"+gp_idx.toString()][chart_id+"_sz"])

  if (chart_id.includes("cost_results")) {
    var mychart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data["Group_"+gp_idx.toString()]["cost_labels"],
         datasets: [{
             axis: 'y',
             label: label,
             data: data["Group_"+gp_idx.toString()][chart_id+"_sz"],
             backgroundColor: [
                   'rgba(255, 99, 132, 0.2)',
                   'rgba(255, 159, 64, 0.2)',
                   'rgba(255, 205, 86, 0.2)',
                   'rgba(75, 192, 192, 0.2)',
                   'rgba(54, 162, 235, 0.2)'
                 ],
             borderColor: [
                   'rgba(255, 99, 132, 0.2)',
                   'rgba(255, 159, 64, 0.2)',
                   'rgba(255, 205, 86, 0.2)',
                   'rgba(75, 192, 192, 0.2)',
                   'rgba(54, 162, 235, 0.2)'
                 ],
            borderWidth: 1
          }]
        },
        options: {
            responsive:true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });

  } else {
    var mychart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data["Group_"+gp_idx.toString()]["labels"],
         datasets: [{
             label: label,
             data: data["Group_"+gp_idx.toString()][chart_id+"_sz"],
             backgroundColor: backgroundColor,
             borderColor: borderColor,
            borderWidth: 1
          }]
        },
        options: {
            responsive:true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
  }
}

function setICERChart(zValues) {
  console.log("!!! Inside setICERChart")
  var xValues = ['Group 1', 'Group 2', 'Group 3', 'Group 4'];

  var yValues = ['Group 4', 'Group 3', 'Group 2', 'Group 1'];

  // var zValues = [
  //   [0.00, 0.00, 0.00, 0.00],
  //   [0.00, 0.00, 0.00, 0.00],
  //   [0.00, 0.00, 0.00, 0.00],
  //   [0.00, 0.00, 0.00, 0.00]
  // ];

  var colorscaleValue = [
    [0, '#5e96ff'],
    [1, '#ff5e5e']
  ];

  var data = [{
    x: xValues.slice(0, zValues.length),
    y: yValues.slice(0, zValues.length),
    z: zValues,
    type: 'heatmap',
    colorscale: colorscaleValue,
    showscale: false
  }];

  var layout = {
    title: 'Annotated Heatmap',
    annotations: [],
    xaxis: {
      ticks: '',
      side: 'top'
    },
    yaxis: {
      ticks: '',
      ticksuffix: ' ',
      width: 700,
      height: 700,
      autosize: false
    }
  };

  for ( var i = 0; i < zValues.length; i++ ) {
    for ( var j = 0; j < zValues.length; j++ ) {
      var currentValue = zValues[i][j];
      if (currentValue != 0.0) {
        var textColor = 'white';
      }else{
        var textColor = 'black';
      }
      var result = {
        xref: 'x1',
        yref: 'y1',
        x: xValues[j],
        y: yValues[i],
        text: zValues[i][j],
        font: {
          family: 'Arial',
          size: 12,
          color: 'rgb(50, 171, 96)'
        },
        showarrow: false,
        font: {
          color: textColor
        }
      };
      layout.annotations.push(result);
    }
  }
  // Plotly.newPlot('tester', data, layout, {staticPlot: true});
  Plotly.newPlot('tester', data, layout);
}









var group_num = 0;
var current_data = {}
var update_data = {}

// Debugging
// console.log("Outside current_data.data: ", current_data)
// console.log("Outsideupdate_data.data: ", update_data)
// console.log("Outside 'api-data/{{analysis_code}}',: ", 'api-data/'+analysis_code)

function isEmpty(obj) {
  for(var prop in obj) {
    if(obj.hasOwnProperty(prop)) {
      return false;
    }
  }

  return JSON.stringify(obj) === JSON.stringify({});
}
console.log("!jQuery.isEmptyObject(update_data): ", !jQuery.isEmptyObject(update_data));

// while (!jQuery.isEmptyObject(update_data)) {
  // console.log("!jQuery.isEmptyObject(update_data): ", !jQuery.isEmptyObject(update_data));
  $.ajax({
      method: 'GET',
      url: 'api-data/'+analysis_code,
      success: function(data){
        // while (data.data != undefined) {
          console.log("Initial analysis_code: ", analysis_code)
          current_data = Object.assign({}, data);
          update_data = Object.assign({}, data);
          console.log("Inside data.data: ", data)
          console.log("Inside current_data.data: ", current_data)
          console.log("Inside update_data.data: ", update_data)
        // }
      },
      error: function(error_data){
        console.log("Initial analysis_code: ", "api-data/"+analysis_code)
        console.log('error');
      }
  })
// }




function update_chart_pannel(activated_idx, vip_pass) {
  console.log("Inside update_chart_pannel!! activated_idx: ", activated_idx)
  console.log("current_data: ", current_data)
  console.log("update_data: ", update_data)
  console.log("JSON.stringify(current_data) != JSON.stringify(update_data): ", JSON.stringify(current_data) != JSON.stringify(update_data))

  // console.log("&& update_data: ", update_data)
  console.log('update_data["Group_" + activated_idx.toString()]: ', update_data["Group_" + activated_idx.toString()])

  var current_day = update_data["Group_" + activated_idx.toString()].labels[update_data["Group_" + activated_idx.toString()].labels.length - 1];
  document.getElementById("g"+activated_idx.toString()+"_current_day_title").innerHTML = '<i class="fas fa-sun" style="margin-left: 10px"></i> &nbsp;' + current_day;


  if (JSON.stringify(current_data) != JSON.stringify(update_data) || vip_pass) {
    console.log("Inside update_chart_pannel!!")
    current_data = Object.assign({}, update_data);
    setChart(update_data, activated_idx, "totalInfected");
    setChart(update_data, activated_idx, "currentInfected");
    setChart(update_data, activated_idx, "newInfected");
    setChart(update_data, activated_idx, "totalSeekMed");
    setChart(update_data, activated_idx, "currentSeekMed");
    setChart(update_data, activated_idx, "newSeekMed");
    setChart(update_data, activated_idx, "totalDeath");
    setChart(update_data, activated_idx, "newDeath");
    setChart(update_data, activated_idx, "totalRecovery");
    setChart(update_data, activated_idx, "newRecovery");
    // setChart(update_data, activated_idx, "totalReachDay");
    // setChart(update_data, activated_idx, "newReachDay");
    setChart(update_data, activated_idx, "cost_results");

    document.getElementById("g"+activated_idx.toString()+"_total_expense_result").innerHTML = "Total Expense: &nbsp" + update_data["Group_" + activated_idx.toString()].total_expanse_sz.toString();
    document.getElementById("g"+activated_idx.toString()+"_total_expense_result").innerHTML = "Total Expense: &nbsp" + update_data["Group_" + activated_idx.toString()].total_expanse_sz.toString();
    document.getElementById("g"+activated_idx.toString()+"_total_expense_result").innerHTML = "Total Expense: &nbsp" + update_data["Group_" + activated_idx.toString()].total_expanse_sz.toString();
    document.getElementById("g"+activated_idx.toString()+"_total_expense_result").innerHTML = "Total Expense: &nbsp" + update_data["Group_" + activated_idx.toString()].total_expanse_sz.toString();

  }
}

function background_fetch_data(group_num){
  console.log("%%%%%%%%%% GROUP_NUM: ", group_num)
  $.ajax({
      method: 'GET',
      url: 'api-data/'+analysis_code,
      success: function(data){
          console.log("1. update analysis_code: ", analysis_code)
          console.log("1.1 data analysis_code: ", data)
          console.log("2. task_status: ", data.task_status)
          update_data = Object.assign({}, data);
          console.log("3. update_data: ", update_data.task_status)

          console.log("Inside 2 data.data: ", data)
          console.log("Inside 2 current_data.data: ", current_data)
          console.log("Inside 2 update_data.data: ", update_data)
          // if ($('#loading_message_container').children().length == 0) {
          //   var load_msg_content = `
          //   <div class="loading" style="backdrop-filter: blur(4px); border-radius: 25px;">
          //     <div class="bounceball" ></div>
          //     &nbsp;
          //     <div class="bounceball2"></div>
          //     &nbsp;
          //     <div class="bounceball3"></div>
          //     <div class="text">&nbsp; RUNNING</div>
          //   </div>
          //   `
          //   document.getElementById("loading_message_container").insertAdjacentHTML('afterbegin', load_msg_content)
          // }
          // if ($('#current_day_title').children().length == 0 && data.labels != null) {


          if (!data.task_status) {
            if ($('#trans_gp_1').hasClass('active')) {
              // document.getElementById("g1_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_1"].total_expanse_sz.toString();
              update_chart_pannel(1, false);
            } else if ($('#trans_gp_2').hasClass('active')) {
              // document.getElementById("g2_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_2"].total_expanse_sz.toString();
              update_chart_pannel(2, false);
            } else if ($('#trans_gp_3').hasClass('active')) {
              // document.getElementById("g3_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_3"].total_expanse_sz.toString();
              update_chart_pannel(3, false);
            } else if ($('#trans_gp_4').hasClass('active')) {
              // document.getElementById("g4_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_4"].total_expanse_sz.toString();
              update_chart_pannel(4, false);
            }
          } else {
            // Success
            // Start from here tomorrow
            console.log("&&& Start parsing ")
            if (data["Group_1"] != undefined) {
              // document.getElementById("g1_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_1"].total_expanse_sz.toString();
              update_chart_pannel(1, true);
            }
            if (data["Group_2"] != undefined) {
              // document.getElementById("g2_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_2"].total_expanse_sz.toString();
              update_chart_pannel(2, true);
            }
            if (data["Group_3"] != undefined) {
              // document.getElementById("g3_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_3"].total_expanse_sz.toString();
              update_chart_pannel(3, true);
            }
            if (data["Group_4"] != undefined) {
              // document.getElementById("g4_total_expense_result").innerHTML = "Total Expense: &nbsp" + data["Group_4"].total_expanse_sz.toString();
              update_chart_pannel(4, true);
            }
            console.log("&&& End parsing ")
            var alert_holding_html = `
            <div class="alert alert-success alert-dismissible fade show" role="alert" style="margin-top:-15px; text-align: center; font-size: 20px">
              <strong>Simulation is finished successfully!</strong>
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            `
            document.getElementById("alert-holding-div").innerHTML = alert_holding_html;
            if ($('#loading_message_container').children().length != 0) {
              const loading_message_node = document.getElementById("loading_message_container");
              loading_message_node.innerHTML = '';
            }
            clearInterval(interval); // stop the interval



            var update_icer = new Array(group_num);
            for (var i = 0; i < update_icer.length; i++) {
              update_icer[i] = new Array(group_num).fill(0.00);
            }
            for (i = 1; i < group_num+1; i++) {
              for (j = 1; j < group_num+1; j++) {
                var i_total_expanse_sz= data["Group_" + i.toString()].total_expanse_sz;
                var i_totalInfected_ls = data["Group_" + i.toString()].totalInfected_sz;
                var i_totalInfected = i_totalInfected_ls[i_totalInfected_ls.length - 1];

                var j_total_expanse_sz= data["Group_" + j.toString()].total_expanse_sz;
                var j_totalInfected_ls = data["Group_" + j.toString()].totalInfected_sz;
                var j_totalInfected = j_totalInfected_ls[j_totalInfected_ls.length - 1];

                console.log(i, " &&&& i_total_expanse_sz: ", i_total_expanse_sz);
                console.log(i, "&&&& i_totalInfected_ls: ", i_totalInfected_ls);
                console.log(i, "&&&& i_totalInfected: ", i_totalInfected);

                console.log(j, "&&&& j_total_expanse_sz: ", j_total_expanse_sz);
                console.log(j, "&&&& j_totalInfected_ls: ", j_totalInfected_ls);
                console.log(j, "&&&& j_totalInfected: ", j_totalInfected);
                icer = (j_total_expanse_sz - i_total_expanse_sz) / (j_totalInfected - i_totalInfected);
                update_icer[group_num-i][j-1] = icer;
              }
            }
            setICERChart(update_icer);
          }
      },
      error: function(error_data){
        console.log('error {{analysis_code}}');
      }
  })
}

if (homepage_status == "running_state" || homepage_status == "post_running_state") {

    if (analysis_code) {
      document.getElementById("analysis_code_canvas").innerHTML = '<div class="alert alert-info alert-dismissible fade show" role="alert" style="margin-top:-30px; text-align: center; font-size: 18px">Your analysis_code is &nbsp &nbsp <strong style="font-size: 22px">'+analysis_code+'</strong></div>'
    }
    // console.log("$('#youth_model').children().length == 0", $('#youth_model').children().length == 0)
    // console.log("$('#adult_model').children().length == 0", $('#adult_model').children().length == 0)
    // console.log("$('#elder_model').children().length == 0", $('#elder_model').children().length == 0)

    // console.log("YOUTH_json_file: ", YOUTH_json_file)
    if ($('#youth_model').children().length == 0) {
      tree("#youth_model", YOUTH_json_file)
    }

    // console.log("ADULT_json_file: ", ADULT_json_file)
    if ($('#adult_model').children().length == 0) {
      tree("#adult_model", ADULT_json_file)
    }

    // console.log("ELDER_json_file: ", ELDER_json_file)
    if ($('#elder_model').children().length == 0) {
      tree("#elder_model", ELDER_json_file)
    }

    // tree("#adult_model", "{{ADULT_json_file}}")
    // tree("#elder_model", "{{ELDER_json_file}}")

      $.ajax({
          method: 'GET',
          async: false,
          url: 'api-params-data/'+analysis_code,
          success: function(params_data){
              group_num = params_data.GROUP_NUM;
              document.getElementById("G1_Vac_YOUTH_Rate_V_txt").innerHTML = params_data.G1_Vac_YOUTH_Rate_V;
              document.getElementById("G1_Vac_ADULT_Rate_V_txt").innerHTML = params_data.G1_Vac_ADULT_Rate_V;
              document.getElementById("G1_Vac_ELDER_Rate_V_txt").innerHTML = params_data.G1_Vac_ELDER_Rate_V;

              document.getElementById("G2_Vac_YOUTH_Rate_V_txt").innerHTML = params_data.G2_Vac_YOUTH_Rate_V;
              document.getElementById("G2_Vac_ADULT_Rate_V_txt").innerHTML = params_data.G2_Vac_ADULT_Rate_V;
              document.getElementById("G2_Vac_ELDER_Rate_V_txt").innerHTML = params_data.G2_Vac_ELDER_Rate_V;

              document.getElementById("G3_Vac_YOUTH_Rate_V_txt").innerHTML = params_data.G3_Vac_YOUTH_Rate_V;
              document.getElementById("G3_Vac_ADULT_Rate_V_txt").innerHTML = params_data.G3_Vac_ADULT_Rate_V;
              document.getElementById("G3_Vac_ELDER_Rate_V_txt").innerHTML = params_data.G3_Vac_ELDER_Rate_V;

              document.getElementById("G4_Vac_YOUTH_Rate_V_txt").innerHTML = params_data.G4_Vac_YOUTH_Rate_V;
              document.getElementById("G4_Vac_ADULT_Rate_V_txt").innerHTML = params_data.G4_Vac_ADULT_Rate_V;
              document.getElementById("G4_Vac_ELDER_Rate_V_txt").innerHTML = params_data.G4_Vac_ELDER_Rate_V;


              document.getElementById("BMP_IDX_CASE_NUM_txt").innerHTML = params_data.BMP_IDX_CASE_NUM;
              document.getElementById("BMP_SIMULATION_DAY_txt").innerHTML = params_data.BMP_SIMULATION_DAY;
              document.getElementById("BMP_CYCLE_DAYS_txt").innerHTML = params_data.BMP_CYCLE_DAYS;
              document.getElementById("BMP_CONTACT_PEOPLE_NUM_txt").innerHTML = params_data.BMP_CONTACT_PEOPLE_NUM;
              document.getElementById("AGP_YOUTH_GRP_txt").innerHTML = params_data.AGP_YOUTH_GRP;
              document.getElementById("AGP_ADULT_GRP_txt").innerHTML = params_data.AGP_ADULT_GRP;
              document.getElementById("AGP_ELDER_GRP_txt").innerHTML = params_data.AGP_ELDER_GRP;
              document.getElementById("CR_SAME_GRP_txt").innerHTML = params_data.CR_SAME_GRP;
              document.getElementById("CR_DIFF_GRP_txt").innerHTML = params_data.CR_DIFF_GRP;
              document.getElementById("Vac_Infection_YOUTH_Rate_V_I_txt").innerHTML = params_data.Vac_Infection_YOUTH_Rate_V_I;
              document.getElementById("Vac_Infection_ADULT_Rate_V_I_txt").innerHTML = params_data.Vac_Infection_ADULT_Rate_V_I;
              document.getElementById("Vac_Infection_ELDER_Rate_V_I_txt").innerHTML = params_data.Vac_Infection_ELDER_Rate_V_I;
              document.getElementById("NoVac_Infection_YOUTH_Rate_NV_I_txt").innerHTML = params_data.NoVac_Infection_YOUTH_Rate_NV_I;
              document.getElementById("NoVac_Infection_ADULT_Rate_NV_I_txt").innerHTML = params_data.NoVac_Infection_ADULT_Rate_NV_I;
              document.getElementById("NoVac_Infection_ELDER_Rate_NV_I_txt").innerHTML = params_data.NoVac_Infection_ELDER_Rate_NV_I;
              document.getElementById("CP_SMT_YOUTH_Rate_CP_txt").innerHTML = params_data.CP_SMT_YOUTH_Rate_CP;
              document.getElementById("CP_SMT_ADULT_Rate_CP_txt").innerHTML = params_data.CP_SMT_ADULT_Rate_CP;
              document.getElementById("CP_SMT_ELDER_Rate_CP_txt").innerHTML = params_data.CP_SMT_ELDER_Rate_CP;
              document.getElementById("CP_SMT_YOUTH_Rate_ST_txt").innerHTML = params_data.CP_SMT_YOUTH_Rate_ST;
              document.getElementById("CP_SMT_ADULT_Rate_ST_txt").innerHTML = params_data.CP_SMT_ADULT_Rate_ST;
              document.getElementById("CP_SMT_ELDER_Rate_ST_txt").innerHTML = params_data.CP_SMT_ELDER_Rate_ST;
              document.getElementById("SMT_IPDOPD_YOUTH_Rate_IPD_txt").innerHTML = params_data.SMT_IPDOPD_YOUTH_Rate_IPD;
              document.getElementById("SMT_IPDOPD_ADULT_Rate_IPD_txt").innerHTML = params_data.SMT_IPDOPD_ADULT_Rate_IPD;
              document.getElementById("SMT_IPDOPD_ELDER_Rate_IPD_txt").innerHTML = params_data.SMT_IPDOPD_ELDER_Rate_IPD;
              document.getElementById("SMT_IPDOPD_YOUTH_Rate_OPD_txt").innerHTML = params_data.SMT_IPDOPD_YOUTH_Rate_OPD;
              document.getElementById("SMT_IPDOPD_ADULT_Rate_OPD_txt").innerHTML = params_data.SMT_IPDOPD_ADULT_Rate_OPD;
              document.getElementById("SMT_IPDOPD_ELDER_Rate_OPD_txt").innerHTML = params_data.SMT_IPDOPD_ELDER_Rate_OPD;
              // document.getElementById("SMT_IPD_Death_YOUTH_Rate_IPD_D_txt").innerHTML = params_data.SMT_IPD_Death_YOUTH_Rate_IPD_D;
              // document.getElementById("SMT_IPD_Death_ADULT_Rate_IPD_D_txt").innerHTML = params_data.SMT_IPD_Death_ADULT_Rate_IPD_D;
              // document.getElementById("SMT_IPD_Death_ELDER_Rate_IPD_D_txt").innerHTML = params_data.SMT_IPD_Death_ELDER_Rate_IPD_D;
              document.getElementById("SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M_txt").innerHTML = params_data.SMT_OPD_MedicineIntake_YOUTH_Rate_OPD_M;
              document.getElementById("SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M_txt").innerHTML = params_data.SMT_OPD_MedicineIntake_ADULT_Rate_OPD_M;
              document.getElementById("SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M_txt").innerHTML = params_data.SMT_OPD_MedicineIntake_ELDER_Rate_OPD_M;
              document.getElementById("SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD_txt").innerHTML = params_data.SMT_OPD_M_IPD_YOUTH_Rate_OPD_M_IPD;
              document.getElementById("SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD_txt").innerHTML = params_data.SMT_OPD_M_IPD_ADULT_Rate_OPD_M_IPD;
              document.getElementById("SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD_txt").innerHTML = params_data.SMT_OPD_M_IPD_ELDER_Rate_OPD_M_IPD;
              document.getElementById("SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D_txt").innerHTML = params_data.SMT_OPD_M_IPD_Death_YOUTH_Rate_OPD_M_IPD_D;
              document.getElementById("SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D_txt").innerHTML = params_data.SMT_OPD_M_IPD_Death_ADULT_Rate_OPD_M_IPD_D;
              document.getElementById("SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D_txt").innerHTML = params_data.SMT_OPD_M_IPD_Death_ELDER_Rate_OPD_M_IPD_D;
              document.getElementById("SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD_txt").innerHTML = params_data.SMT_OPD_NM_IPD_YOUTH_Rate_OPD_NM_IPD;
              document.getElementById("SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD_txt").innerHTML = params_data.SMT_OPD_NM_IPD_ADULT_Rate_OPD_NM_IPD;
              document.getElementById("SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD_txt").innerHTML = params_data.SMT_OPD_NM_IPD_ELDER_Rate_OPD_NM_IPD;
              document.getElementById("SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D_txt").innerHTML = params_data.SMT_OPD_NM_IPD_Death_YOUTH_Rate_OPD_NM_IPD_D;
              document.getElementById("SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D_txt").innerHTML = params_data.SMT_OPD_NM_IPD_Death_ADULT_Rate_OPD_NM_IPD_D;
              document.getElementById("SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D_txt").innerHTML = params_data.SMT_OPD_NM_IPD_Death_ELDER_Rate_OPD_NM_IPD_D;
              document.getElementById("MC_YOUTH_EARN_LOST_PER_DEATH_Rate_txt").innerHTML = params_data.MC_YOUTH_EARN_LOST_PER_DEATH_Rate;
              document.getElementById("MC_ADULT_EARN_LOST_PER_DEATH_Rate_txt").innerHTML = params_data.MC_ADULT_EARN_LOST_PER_DEATH_Rate;
              document.getElementById("MC_ELDER_EARN_LOST_PER_DEATH_Rate_txt").innerHTML = params_data.MC_ELDER_EARN_LOST_PER_DEATH_Rate;
              document.getElementById("TIC_YOUTH_AVE_STAY_DAY_Rate_txt").innerHTML = params_data.TIC_YOUTH_AVE_STAY_DAY_Rate;
              document.getElementById("TIC_ADULT_AVE_STAY_DAY_Rate_txt").innerHTML = params_data.TIC_ADULT_AVE_STAY_DAY_Rate;
              document.getElementById("TIC_ELDER_AVE_STAY_DAY_Rate_txt").innerHTML = params_data.TIC_ELDER_AVE_STAY_DAY_Rate;
              document.getElementById("TIC_YOUTH_COST_PER_BED_PER_DAY_Rate_txt").innerHTML = params_data.TIC_YOUTH_COST_PER_BED_PER_DAY_Rate;
              document.getElementById("TIC_ADULT_COST_PER_BED_PER_DAY_Rate_txt").innerHTML = params_data.TIC_ADULT_COST_PER_BED_PER_DAY_Rate;
              document.getElementById("TIC_ELDER_COST_PER_BED_PER_DAY_Rate_txt").innerHTML = params_data.TIC_ELDER_COST_PER_BED_PER_DAY_Rate;
              document.getElementById("TIC_YOUTH_HOS_LOSS_PER_DAY_Rate_txt").innerHTML = params_data.TIC_YOUTH_HOS_LOSS_PER_DAY_Rate;
              document.getElementById("TIC_ADULT_HOS_LOSS_PER_DAY_Rate_txt").innerHTML = params_data.TIC_ADULT_HOS_LOSS_PER_DAY_Rate;
              document.getElementById("TIC_ELDER_HOS_LOSS_PER_DAY_Rate_txt").innerHTML = params_data.TIC_ELDER_HOS_LOSS_PER_DAY_Rate;
              document.getElementById("TIC_YOUTH_TRANS_COST_Rate_txt").innerHTML = params_data.TIC_YOUTH_TRANS_COST_Rate;
              document.getElementById("TIC_ADULT_TRANS_COST_Rate_txt").innerHTML = params_data.TIC_ADULT_TRANS_COST_Rate;
              document.getElementById("TIC_ELDER_TRANS_COST_Rate_txt").innerHTML = params_data.TIC_ELDER_TRANS_COST_Rate;
              document.getElementById("TOC_YOUTH_AVE_DAY_LOST_Rate_txt").innerHTML = params_data.TOC_YOUTH_AVE_DAY_LOST_Rate;
              document.getElementById("TOC_ADULT_AVE_DAY_LOST_Rate_txt").innerHTML = params_data.TOC_ADULT_AVE_DAY_LOST_Rate;
              document.getElementById("TOC_ELDER_AVE_DAY_LOST_Rate_txt").innerHTML = params_data.TOC_ELDER_AVE_DAY_LOST_Rate;
              document.getElementById("TOC_YOUTH_TREAT_COST_Rate_txt").innerHTML = params_data.TOC_YOUTH_TREAT_COST_Rate;
              document.getElementById("TOC_ADULT_TREAT_COST_Rate_txt").innerHTML = params_data.TOC_ADULT_TREAT_COST_Rate;
              document.getElementById("TOC_ELDER_TREAT_COST_Rate_txt").innerHTML = params_data.TOC_ELDER_TREAT_COST_Rate;
              document.getElementById("TOC_YOUTH_OPD_LOST_PER_DAY_Rate_txt").innerHTML = params_data.TOC_YOUTH_OPD_LOST_PER_DAY_Rate;
              document.getElementById("TOC_ADULT_OPD_LOST_PER_DAY_Rate_txt").innerHTML = params_data.TOC_ADULT_OPD_LOST_PER_DAY_Rate;
              document.getElementById("TOC_ELDER_OPD_LOST_PER_DAY_Rate_txt").innerHTML = params_data.TOC_ELDER_OPD_LOST_PER_DAY_Rate;
              document.getElementById("TOC_YOUTH_TRANS_COST_Rate_txt").innerHTML = params_data.TOC_YOUTH_TRANS_COST_Rate;
              document.getElementById("TOC_ADULT_TRANS_COST_Rate_txt").innerHTML = params_data.TOC_ADULT_TRANS_COST_Rate;
              document.getElementById("TOC_ELDER_TRANS_COST_Rate_txt").innerHTML = params_data.TOC_ELDER_TRANS_COST_Rate;
              document.getElementById("TVC_YOUTH_VAC_COST_Rate_txt").innerHTML = params_data.TVC_YOUTH_VAC_COST_Rate;
              document.getElementById("TVC_ADULT_VAC_COST_Rate_txt").innerHTML = params_data.TVC_ADULT_VAC_COST_Rate;
              document.getElementById("TVC_ELDER_VAC_COST_Rate_txt").innerHTML = params_data.TVC_ELDER_VAC_COST_Rate;
              document.getElementById("TVC_YOUTH_VAC_LOST_PER_HOUR_Rate_txt").innerHTML = params_data.TVC_YOUTH_VAC_LOST_PER_HOUR_Rate;
              document.getElementById("TVC_ADULT_VAC_LOST_PER_HOUR_Rate_txt").innerHTML = params_data.TVC_ADULT_VAC_LOST_PER_HOUR_Rate;
              document.getElementById("TVC_ELDER_VAC_LOST_PER_HOUR_Rate_txt").innerHTML = params_data.TVC_ELDER_VAC_LOST_PER_HOUR_Rate;
              document.getElementById("TVC_YOUTH_TRANS_COST_Rate_txt").innerHTML = params_data.TVC_YOUTH_TRANS_COST_Rate;
              document.getElementById("TVC_ADULT_TRANS_COST_Rate_txt").innerHTML = params_data.TVC_ADULT_TRANS_COST_Rate;
              document.getElementById("TVC_ELDER_TRANS_COST_Rate_txt").innerHTML = params_data.TVC_ELDER_TRANS_COST_Rate;
              document.getElementById("TVC_YOUTH_EFF_txt").innerHTML = params_data.TVC_YOUTH_EFF;
              document.getElementById("TVC_ADULT_EFF_txt").innerHTML = params_data.TVC_ADULT_EFF;
              document.getElementById("TVC_ELDER_EFF_txt").innerHTML = params_data.TVC_ELDER_EFF;
              document.getElementById("TVSEC_YOUTH_SIDE_EFF_Rate_txt").innerHTML = params_data.TVSEC_YOUTH_SIDE_EFF_Rate;
              document.getElementById("TVSEC_ADULT_SIDE_EFF_Rate_txt").innerHTML = params_data.TVSEC_ADULT_SIDE_EFF_Rate;
              document.getElementById("TVSEC_ELDER_SIDE_EFF_Rate_txt").innerHTML = params_data.TVSEC_ELDER_SIDE_EFF_Rate;
              document.getElementById("TVSEC_YOUTH_MEAN_OPD_FREQ_Rate_txt").innerHTML = params_data.TVSEC_YOUTH_MEAN_OPD_FREQ_Rate;
              document.getElementById("TVSEC_ADULT_MEAN_OPD_FREQ_Rate_txt").innerHTML = params_data.TVSEC_ADULT_MEAN_OPD_FREQ_Rate;
              document.getElementById("TVSEC_ELDER_MEAN_OPD_FREQ_Rate_txt").innerHTML = params_data.TVSEC_ELDER_MEAN_OPD_FREQ_Rate;
              document.getElementById("TVSEC_YOUTH_DIR_OPD_COST_Rate_txt").innerHTML = params_data.TVSEC_YOUTH_DIR_OPD_COST_Rate;
              document.getElementById("TVSEC_ADULT_DIR_OPD_COST_Rate_txt").innerHTML = params_data.TVSEC_ADULT_DIR_OPD_COST_Rate;
              document.getElementById("TVSEC_ELDER_DIR_OPD_COST_Rate_txt").innerHTML = params_data.TVSEC_ELDER_DIR_OPD_COST_Rate;
              document.getElementById("TVSEC_YOUTH_PROD_OPD_LOSS_Rate_txt").innerHTML = params_data.TVSEC_YOUTH_PROD_OPD_LOSS_Rate;
              document.getElementById("TVSEC_ADULT_PROD_OPD_LOSS_Rate_txt").innerHTML = params_data.TVSEC_ADULT_PROD_OPD_LOSS_Rate;
              document.getElementById("TVSEC_ELDER_PROD_OPD_LOSS_Rate_txt").innerHTML = params_data.TVSEC_ELDER_PROD_OPD_LOSS_Rate;
              document.getElementById("TVSEC_YOUTH_TRANS_COST_Rate_txt").innerHTML = params_data.TVSEC_YOUTH_TRANS_COST_Rate;
              document.getElementById("TVSEC_ADULT_TRANS_COST_Rate_txt").innerHTML = params_data.TVSEC_ADULT_TRANS_COST_Rate;
              document.getElementById("TVSEC_ELDER_TRANS_COST_Rate_txt").innerHTML = params_data.TVSEC_ELDER_TRANS_COST_Rate;
          },
          error: function(error_data){
            console.log('error');
          }
      })

    // var default_icer = [
    //   [0.00, 0.10, 0.20, 0.30],
    //   [0.40, 0.50, 0.60, 0.70],
    //   [0.80, 1.00, 0.00, 0.00],
    //   [0.11, 0.00, 0.00, 0.00]
    // ];

    var default_icer = new Array(group_num);

    for (var i = 0; i < default_icer.length; i++) {
      default_icer[i] = new Array(group_num).fill(0.00);
    }
    console.log("** default_icer: ", default_icer);

    setICERChart(default_icer);
    var interval = null;
    interval = setInterval(background_fetch_data, 1500, group_num);
}
