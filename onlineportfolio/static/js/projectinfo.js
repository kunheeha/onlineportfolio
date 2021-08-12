$(document).ready(function() {

	$('.allNotes').on('click', function() {
		$('.activeNote').removeClass('activeNote');
		$(this).addClass('activeNote');
		let activeNoteID = $(this).attr('data-noteid');
		$('.notes').addClass('inactiveNote');
		$(`#${activeNoteID}`).removeClass('inactiveNote');
	})

})
