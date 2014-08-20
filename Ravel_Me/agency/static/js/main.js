        
$(document).ready(function(){
	$('#form-recommend').submit(function(event) {			
		event.preventDefault();
		console.log( $(this).serialize() )
		$.ajax('projects',
			{data: $(this).serialize()+'&'+$('#form-cats').serialize(),
			success: function(data) {
				projects = data.projects;
                $("#projectbox tr").remove();
                 for (i=0; i < projects.length; i++) {
					$("#projectbox table").append('<tr><td>' + projects[i]['pic'] + '</td><td>' + projects[i]['name'] + '</td></tr>'); 
				}
			}
		})
	})
})

$(document).ready(function(){
	$('#ravelme').click( function() {
		$('#form-recommend').submit() 
	})
	$('input:radio[name=craft]').click( function() {
		$('#form-recommend').submit() 
	})
	$('input:radio[name=category]').click( function() {
		$('#form-recommend').submit() 
	})
})
	













