$(document).ready(function(){

  $("#issue-popup").hide();
  let inner_card = $('.inner-card');
  //clone the issue form
  let clonedIssueForm= inner_card[inner_card.length - 1].cloneNode(true);
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
    //Regex to find all instances of the form number
    let formRegex = RegExp(`issues_set-(\\d){1}-`,'g');
    //Increment the form number
    formNum++;
    console.log(formNum);

    newForm ="<div class='inner-card'>" +
    newForm.innerHTML.replace(formRegex, `form-${formNum}-`) +
    "</div>";//Update the new form to have the correct form number

    function get_vuln_data(){
        let ajax_url = $('#issue-title').attr("data-ajax_url");
        let value = $('#issue-title').val();
        let formData = null;
        $.ajax({
            url: ajax_url,
            data: {
              'search_val': value
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
    container.append(newForm);
    totalForms.attr('value', `${formNum+1}`);

    //get the same form
    let lastAppended = inner_card.last();
    //get vulnerability data
    let formData = get_vuln_data();
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