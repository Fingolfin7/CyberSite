$(document).ready(function(){
  let container = $("#issues-div");
  let appendButton = $("#append-issue");

  $("#close").click(function(){
      $("#issue-popup").hide();
  });

  appendButton.click((e)=>{
    e.preventDefault();

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

    let formData = get_vuln_data(); //get vulnerability data

    if(formData){
        //set form values
        container.find('.issueName').val(formData['title']);
        container.find('.issueSeverity').val(formData['severity']);
        container.find('.issueDescription').val(formData['description']);
        container.find('.issueReference').val(formData['reference']);
        container.find('.issueRating').val(formData['cvss_rating']);
    }
    else{
        container.find('.issueName').val($('#issue-title').val());
    }

    $("#issue-popup").hide();
  });
});

