$(document).ready(function () {
    var sidebar = $('.sidebar');
    var toggleSidebar = $('#toggle-sidebar');
    $('.following-content').hide();

    toggleSidebar.click(function () {
        if (sidebar.css('left') === '-250px') {
            sidebar.animate({left: '0'}, 500);
        } else {
            sidebar.animate({left: '-250px'}, 500);
        }
    });

    $('#toggle-following').click(function () {
        $('#toggle-foryou').removeClass("selected");
        $('.foryou').hide();
        $('.following-content').show();
        $('#toggle-following').addClass("selected");

    });
    $('#toggle-foryou').click(function () {
        $('#toggle-following').removeClass("selected");
        $('.following-content').hide();
        $('.foryou').show();
        $('#toggle-foryou').addClass("selected");
    });

    $(document).on('click', function (event) {
        // verifica se o usuário clicou no menu suspenso ou em um elemento filho
        if (!$(event.target).closest('.dropdown').length) {
            // oculta o menu suspenso
            $('.dropdown-content').hide();
        }
    });

    $('.dropdown').on('click', function () {
        // exibe ou oculta o menu suspenso quando o usuário clica no botão
        $('.dropdown-content').toggle();
    });

    $('#moviescheck').click(function () {
        $('.search-results-movies').toggle();
    });
    $('#reviewerscheck').click(function () {
        $('.search-results-reviewers').toggle();
    });
    $('#genrecheck').click(function () {
        $('.search-container').toggle();
    });

    $('#register-checkbox').click(function () {
        if ($('#register-checkbox').is(':checked')) {
            $('#register-form').removeClass('hidden');
            $('#login-form').addClass('hidden');
        } else {
            $('#register-form').addClass('hidden');
            $('#login-form').removeClass('hidden');
        }
    });

    $('#login-checkbox').click(function () {
        if ($('#login-checkbox').is(':checked')) {
            $('#login-form').removeClass('hidden');
            $('#register-form').addClass('hidden');
        } else {
            $('#login-form').addClass('hidden');
            $('#register-form').removeClass('hidden');
        }
    });

    var stars = document.querySelectorAll(".star");
    var ratingValue = 0;

    for (var i = 0; i < stars.length; i++) {
        stars[i].addEventListener("mouseover", function (event) {
            var currentStar = event.target;
            var previousStars = currentStar;

            while (previousStars) {
                previousStars.classList.add("selected");
                previousStars = previousStars.previousElementSibling;
            }
        });

        stars[i].addEventListener("mouseout", function (event) {
            var currentStar = event.target;
            var previousStars = currentStar;
            if (ratingValue == 0) {
                while (previousStars) {
                    previousStars.classList.remove("selected");
                    previousStars = previousStars.previousElementSibling;
                }
            }
        });
        stars[i].addEventListener("click", function (event) {
            var currentStar = event.target;
            ratingValue = currentStar.getAttribute('data-value');
            var nextStars = event.target.nextElementSibling;
            document.getElementById("rating").value = ratingValue;
            while (nextStars) {
                nextStars.classList.remove("selected");
                nextStars = nextStars.nextElementSibling;
            }
        });
    }

});

function exibirOpcoes() {
    var opcoesCheckbox = document.getElementById("opcoesCheckbox");
    if (opcoesCheckbox.style.display === "none") {
        opcoesCheckbox.style.display = "block";
    } else {
        opcoesCheckbox.style.display = "none";
    }
}

function atualizarOpcoesSelecionadas() {
    var opcoesSelecionadas = document.getElementById("opcoesSelecionadas");
    var opcoes = document.getElementsByName("opcoes");
    var opcoesSelecionadasArray = [];
    for (var i = 0; i < opcoes.length; i++) {
        if (opcoes[i].checked) {
            opcoesSelecionadasArray.push(opcoes[i].value);
        }
    }
    opcoesSelecionadas.value = opcoesSelecionadasArray.join(", ");
}

  function mostrarSenha(id) {
        var senhaInput = document.getElementById(id);
        if (senhaInput.type === "password") {
            senhaInput.type = "text";
        } else {
            senhaInput.type = "password";
        }
    }