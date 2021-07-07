var self_js_script = $('script[src*=post_groups_switching]'); // or better regexp to get the file name..
var analysis_code = self_js_script.attr('analysis_code');

console.log("**** self_js_script: ", self_js_script)
console.log("**** analysis_code: ", analysis_code)

$.ajax({
    method: 'GET',
    url: 'api-params-data/'+analysis_code,
    success: function(param_data){
        console.log("Initial analysis_code: ", analysis_code)
        // current_data = Object.assign({}, data);
        console.log("INSIDE!!!")
        console.log("GROUP_NUM: ", param_data.GROUP_NUM)
        if (param_data.GROUP_NUM >= 2) {
          document.getElementById("trans_gp_2").style.display = "block";
        }
        if (param_data.GROUP_NUM >= 3) {
          document.getElementById("trans_gp_3").style.display = "block";
        }
        if (param_data.GROUP_NUM >= 4) {
          document.getElementById("trans_gp_4").style.display = "block";
        }
    },
    error: function(error_data){
      console.log("Initial analysis_code: ", "api-data/"+analysis_code)
      console.log('error');
    }
})
