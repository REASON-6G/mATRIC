    $(function(){
        $("button[name='deletebtn']").click(function() {
        $(this).prop("disabled",true);
        $(this).click(false);
        var id = $(this).attr("data-user-id");
    	$.ajax({
    			url: $SCRIPT_ROOT + 'manageusers/' + id,
    			type: 'DELETE',
    			beforeSend: function(){
    			    // Show image container
    			    $('#'+ id + '_trashicon').hide();
    			    $('#'+ id + '_loader').show();
    			   },
    			success: function(response){
    				if (response['result'] == 200){
    					$('#' + id + '_row').remove();
    					console.log(response['message']);
    			        $('#alert_message').clone().prop("id","userdelete").insertAfter('.alert').addClass("alert-success").append("<span>"+response['message']+"</span>").slideDown('fast').delay(6000).slideUp('slow', function(){
	        				$('#userdelete').remove();
	        			}); 
    				}else{
    				   console.log(response['message']);
    				    $('#'+ id + '_trashicon').show();
    			        $('#'+ id + '_loader').hide();
        			    $(this).prop("disabled",false);
        			    $(this).click(true);
    			        $('#alert_message').clone().prop("id","userdelete").insertAfter('.alert').addClass("alert-danger").append("<span>"+response['message']+"</span>").slideDown('fast').delay(6000).slideUp('slow', function(){
	        				$('#userdelete').remove();
	        			}); 
    				}
    			},
    			error: function(error){
    			    $('#'+ id + '_trashicon').show();
    			    $('#'+ id + '_loader').hide();
    			    $(this).prop("disabled",false);
        			$(this).click(true);
    				console.log(error);
     			    $('#alert_message').clone().prop("id","userdelete").insertAfter('.alert').addClass("alert-success").append("<span>"+error+"</span>").slideDown('fast').delay(6000).slideUp('slow', function(){
	        			$('#userdelete').remove();
	        		}); 
    		    },
    		});
    	});
      });
      
      $(function(){
        $("select[name='permlevel']").change(function() {
        var id = $(this).attr("data-user-id");
        var permlevel = $(this).val();
        
    	$.ajax({
    			url: $SCRIPT_ROOT + 'manageusers/' + id + '/permlevel/' + permlevel,
    			type: 'POST',
    			success: function(response){
    				if (response['result'] == 200){
    					console.log(response['message']);
    			        $('#alert_message').clone().prop("id","permchanged").insertAfter('.alert').addClass("alert-success").append("<span>"+response['message']+"</span>").slideDown('fast').delay(6000).slideUp('slow', function(){
	        				$('#permchanged').remove();
	        			}); 
	        		}else{
    				   console.log(response['message']);
    			        $('#alert_message').clone().prop("id","permchanged").insertAfter('.alert').addClass("alert-danger").append("<span>"+response['message']+"</span>").slideDown('fast').delay(6000).slideUp('slow', function(){
	        				$('#permchanged').remove();
	        			});  
	    			}
    			},
    			error: function(error){
    				console.log(error);
    			}
    		});
    	});
    	
        $("select[name='active']").change(function() {
        var id = $(this).attr("data-user-id");
        var active = $(this).val();
        
    	$.ajax({
    			url: $SCRIPT_ROOT + 'manageusers/' + id + '/active/' + active,
    			type: 'POST',
    			success: function(response){
    				if (response['result'] == 200){
    					console.log(response['message']);
    			        $('#alert_message').clone().prop("id","activated").insertAfter('.alert').addClass("alert-success").append("<span>"+response['message']+"</span>").slideDown('fast').delay(6000).slideUp('slow', function(){
	        				$('#activated').remove();
	        			});       				
	        		}else{
    				   console.log(response['message']);
    			        $('#alert_message').clone().prop("id","activated").insertAfter('.alert').addClass("alert-danger").append("<span>"+response['message']+"</span>").slideDown('fast').delay(6000).slideUp('slow', function(){
	        				$('#activated').remove();
	        			});  
	    			}
    			},
    			error: function(error){
    				console.log(error);
    			}
    		});
    	});
    	
 

    	
      });