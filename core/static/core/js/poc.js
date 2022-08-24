$(document).ready(function(){
  let container = $('.poc_flex_section');
  let appendPoc = $("#append-poc");
  let poc_table = $('.poc_table');
  let clonedIssueForm= poc_table[poc_table.length - 1].cloneNode(true);  //clone the upload input
  let totalForms = $("#id_poc_set-TOTAL_FORMS");
  let formNum = $('.poc_table').length - 1;

  appendPoc.click((e)=>{
    e.preventDefault();
    let newForm = clonedIssueForm;
    let formRegex = RegExp(`poc_set-(\\d){1}-`,'g'); //Regex to find all instances of the form number
    formNum++; //Increment the form number

    newForm ="<table class='poc_table'>" +
    newForm.innerHTML.replace(formRegex, `poc_set-${formNum}-`) +
    "</table>";//Update the new form to have the correct form number

    //append empty issue form
    container.append(newForm);
    totalForms.attr('value', `${formNum+1}`);
  });
});