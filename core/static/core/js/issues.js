$(document).ready(function(){
  $("#issue-popup").hide();
  $("#chart").hide();

  let inner_card = $('.inner-card');
  let clonedIssueForm= inner_card[inner_card.length - 1].cloneNode(true); //clone the issue form
  let container = $("#issues-div");
  let appendButton = $("#append-issue");
  let totalForms = $("#id_issues_set-TOTAL_FORMS");
  let formNum = $('.inner-card').length - 1;

  $("#add-issue").click(function(){
    $("#issue-popup").show();
    $("#issue-sources").css("width", "40%");
    $("#issue-title").css({"width":"90%", "margin": "2rem 0rem 2rem 0rem",
    "padding" : "0.4rem", "border": "medium solid forestgreen",
    "border-radius": "0.4rem"});
    $("#issue-title").val("");
  });

  $("#cancel").click(function(){
      $("#issue-popup").hide();
  });

  appendButton.click((e)=>{
    e.preventDefault();
    let newForm = clonedIssueForm;
    let formRegex = RegExp(`issues_set-(\\d){1}-`,'g'); //Regex to find all instances of the form number
    formNum++; //Increment the form number

    newForm ="<div class='inner-card'>" +
    newForm.innerHTML.replace(formRegex, `issues_set-${formNum}-`) +
    "</div>";//Update the new form to have the correct form number

    function get_vuln_data(){
        let ajax_url = $('#issue-title').attr("data-ajax_url");
        let vuln_source = $("#issue-sources").val();
        let value = $('#issue-title').val();
        let formData = null;
        $.ajax({
            url: ajax_url,
            data: {
              'search_val': value,
              'vuln_source': vuln_source
            },
            dataType: 'json',
            async: false,
            cache: false,
            success: function (data) {
                formData = data.results.filter((el)=>{
                    if(el['title'] == value){
                        return el;
                    }
                });

                formData = formData[0];
                //console.log(formData['title']);
            }
        });
        return formData;
    }

    //append empty issue form
    container.prepend(newForm);
    totalForms.attr('value', `${formNum+1}`);

    let lastAppended = $('.inner-card').last(); //get the same form
    let formData = get_vuln_data(); //get vulnerability data
    if(formData){
        //set form values
        lastAppended.find('.issueName').val(formData['title']);
        lastAppended.find('.issueSeverity').val(formData['severity']);
        lastAppended.find('.issueDescription').val(formData['desc']);
        lastAppended.find('.issueReference').val(formData['ref']);
        lastAppended.find('.issueRating').val(formData['cvss']);
    }
    else{
        lastAppended.find('.issueName').val($('#issue-title').val());
    }
    //console.log(totalForms.val());
    $("#issue-popup").hide();
  });


  $("#view_stats").click(function(){
    $("#chart").toggle("slow");
    $("#issues-div").toggle("slow");
    $("#add-issue").toggle("slow");
  });
});

function edit_dropdown(issue){
  dropdown_icon = issue.children("i").text();

  if(dropdown_icon == "keyboard_arrow_down"){
    issue.children("i").text("keyboard_arrow_up");
  }
  else{
    issue.children("i").text("keyboard_arrow_down");
  }

  var thisIssue = issue.closest(".inner-card");
  var issueDropdown = thisIssue.children(".dropdown-content");
  issueDropdown.toggle("slow");

}

function preview(input){
  var inputID = input.attr("id");
  var img_preview = input.closest(".dropdown-content").children(`#preview-${inputID}`);
  console.log(img_preview);
  img_preview.empty();

  if($(input)[0].files){
    for(var i = 0; i < $(input)[0].files.length; i++){
      var img_src = URL.createObjectURL($(input)[0].files[i]);
      URL.revokeObjectURL($(input)[0].files[i]); // free up memory
      var img_name = $(input)[0].files[i].name;

      img_preview.append(`<img src="${img_src}" alt="${img_name}"
      style="max-height: 100px;
      border: 2px solid lightgrey;
      margin-right: 2%;"/>`);
    }

  }
  else{
    console.log(`Nope! ${$(input)[0].files}`);
  }
}