$("#testing_submit_button").click(function(event) {

    let question_inputs = $("input.question_text_input");

    let question_count = 0;

    question_inputs.each(function(i,elem) {
        let question = $(this);
        let change_answer_type_select = question.parents('.question_text_input_div').siblings('.change_answer_type_select_div').find('.change_answer_type_select');
        question.attr('name', 'question_input_text_' + i);
        change_answer_type_select.attr('name', 'question_answer_type_select_' + i);
        let answer_div = question.parents('.row').siblings('.answers_div');
        let answers_inputs = answer_div.find('.answer_text_input');
        let answer_count = 0;

        answers_inputs.each(function(j,elem) {
            $(this).attr('name', 'question_' + i + '_answer_' + j);
            let is_true_input = $(this).parents('td').siblings('.is_true_td').find('.is_true_input');
            if (change_answer_type_select.children("option:selected").val() == 1) {
                is_true_input.attr('name', 'question_' + i + '_answer_is_true_input');
                is_true_input.attr('value', $(this).val());
            }
            else if (change_answer_type_select.children("option:selected").val() == 2) {
                is_true_input.attr('name', 'question_' + i + '_answer_is_true_input_' + j);
            }

            answer_count = answer_count + 1;
        });

        answer_div.find('.answer_count').remove();
        let answer_count_input = `<input type="hidden" name="question_${i}_answer_count" class="answer_count" value=${answer_count}>`;
        answer_div.append(answer_count_input);
        question_count = question_count + 1;
    });

    $('form').find('#id_question_count').remove();
    let question_count_input = `<input type="hidden" name="question_count" id="id_question_count" value=${question_count}>`;
    $('form').append(question_count_input);

    let form = document.getElementsByClassName('needs-validation');
    if (form[0].checkValidity() === true) {
        form[0].submit();
    }
    form[0].classList.add('was-validated');

});