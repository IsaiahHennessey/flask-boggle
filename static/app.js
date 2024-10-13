class BoggleGame {
    constructor(timeLimit = 60) {
        this.score = 0;
        this.words = new Set();
        this.timeRemaining = timeLimit;
        this.timerInterval = null;
        this.setup();
    }

    setup() {
        this.updateTimer();
        this.timerInterval = setInterval(this.updateTimer.bind(this), 1000);
        $('#word-form').on('submit', this.handleSubmit.bind(this));
    }

    async handleSubmit(evt) {
        evt.preventDefault();
        if (this.timeRemaining <= 0) return;

        const word = $('#word-input').val();
        if (!word) return;
        $('#word-input').val('');

        if (this.words.has(word)) {
            $('#result').text(`"${word}" has already been used.`);
            return;
        }

        try {
            const response = await axios.get('/check-word', { params: { word } });
            this.processWordResponse(word, response.data.result);
        } catch (err) {
            console.error('Error checking word:', err);
            $('#result').text('An error occurred. Please try again.');
        }
    }

    processWordResponse(word, result) {
        if (result === 'ok') {
            this.words.add(word);
            this.updateScore(word.length);
            $('#result').text(`"${word}" is a valid word!`);
        } else if (result === 'not-on-board') {
            $('#result').text(`"${word}" is not on the board.`);
        } else {
            $('#result').text(`"${word}" is not a valid word.`);
        }
    }

    updateScore(points) {
        this.score += points;
        $('#score').text(this.score);
    }

    updateTimer() {
        this.timeRemaining -= 1;
        $('#timer').text(this.timeRemaining);

        if (this.timeRemaining <= 0) {
            clearInterval(this.timerInterval);
            $('#word-form :input').prop('disabled', true);
            $('#result').text('Time is up!');
            this.sendScoreToServer();
        }
    }

    async sendScoreToServer() {
        try {
            const response = await axios.post('/post-score', { score: this.score });
            const { times_played, high_score } = response.data;
            $('#result').append(`<p>Games Played: ${times_played}</p>`);
            $('#result').append(`<p>High Score: ${high_score}</p>`);
        } catch (err) {
            console.error('Error posting score:', err);
        }
    }
}

$(document).ready(function() {
    $('#word-form').on('submit', function(event) {
        event.preventDefault();
        let word = $('#word_input').val();

        $.get('/check-word', { word: word }, function(data) {
            $('#result').text(data.result);
            $('#word_input').val('');
        });
    });
});

