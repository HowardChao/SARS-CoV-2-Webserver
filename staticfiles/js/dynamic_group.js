function checkGroupNum () {
  var trans_gp_1 = document.getElementById('trans_gp_1');
  var trans_gp_2 = document.getElementById('trans_gp_2');
  var trans_gp_3 = document.getElementById('trans_gp_3');
  var trans_gp_4 = document.getElementById('trans_gp_4');
  var GROUP_NUM_DYNAMIC = 0;
  if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "none" && trans_gp_3.style.display == "none" && trans_gp_4.style.display == "none") {
    GROUP_NUM_DYNAMIC = 1;
  } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "none" && trans_gp_4.style.display == "none") {
    GROUP_NUM_DYNAMIC = 2;
  } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "block" && trans_gp_4.style.display == "none") {
    GROUP_NUM_DYNAMIC = 3;
  } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "block" && trans_gp_4.style.display == "block") {
    GROUP_NUM_DYNAMIC = 4;
  }
  // console.log("Inside checkGroupNum: ")
  // document.getElementById("DISPLAY").innerHTML = GROUP_NUM_DYNAMIC;
  document.getElementById("GROUP_NUM_INPUT").value = GROUP_NUM_DYNAMIC;
}

function addExpGp() {
  // console.log("Inside addExpGp: ")
  $('#alert_maximum_group_num_reached').fadeOut();
  $('#alert_minimum_group_num_reached').fadeOut();
  $('#current_active_remove_fail').fadeOut();
   var trans_gp_1 = document.getElementById('trans_gp_1');
   var trans_gp_2 = document.getElementById('trans_gp_2');
   var trans_gp_3 = document.getElementById('trans_gp_3');
   var trans_gp_4 = document.getElementById('trans_gp_4');
   if(trans_gp_1.style.display == "block" && trans_gp_2.style.display == "none") {
     trans_gp_2.style.display = "block";
   } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "none") {
     trans_gp_3.style.display = "block";
   } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "block" && trans_gp_4.style.display == "none") {
     trans_gp_4.style.display = "block";
   } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "block" && trans_gp_4.style.display == "block") {
     console.log("You cannot add more group!!!")
     $('#alert_maximum_group_num_reached').fadeIn();
   }
   checkGroupNum()
}



function removeExpGp() {
  // console.log("Inside removeExpGp: ")
  $('#alert_maximum_group_num_reached').fadeOut();
  $('#alert_minimum_group_num_reached').fadeOut();
  $('#current_active_remove_fail').fadeOut();
   var trans_gp_1 = document.getElementById('trans_gp_1');
   var trans_gp_2 = document.getElementById('trans_gp_2');
   var trans_gp_3 = document.getElementById('trans_gp_3');
   var trans_gp_4 = document.getElementById('trans_gp_4');
   if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "none" && trans_gp_3.style.display == "none" && trans_gp_4.style.display == "none") {
     $('#alert_minimum_group_num_reached').fadeIn();
   } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "none") {
     if (! trans_gp_2.classList.contains('active')) {
       trans_gp_2.style.display = "none";
     } else {
       console.log("trans_gp_2 is active and cannot be removed.")
       $('#current_active_remove_fail').fadeIn();
     }
   } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "block" && trans_gp_4.style.display == "none") {
     if (! trans_gp_3.classList.contains('active')) {
       trans_gp_3.style.display = "none";
     } else {
       console.log("trans_gp_3 is active and cannot be removed.")
       $('#current_active_remove_fail').fadeIn();
     }
   } else if (trans_gp_1.style.display == "block" && trans_gp_2.style.display == "block" && trans_gp_3.style.display == "block" && trans_gp_4.style.display == "block") {
     if (! trans_gp_4.classList.contains('active')) {
       trans_gp_4.style.display = "none";
     } else {
       console.log("trans_gp_4 is active and cannot be removed.")
       $('#current_active_remove_fail').fadeIn();
     }
   }
   checkGroupNum()
}
