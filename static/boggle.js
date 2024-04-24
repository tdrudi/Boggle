class BoggleGame{
    //Make a new game
    constructor(boardId, seconds = 60){
        this.seconds = seconds;
        this.showTime();
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        this.timer = setInterval(this.countdown.bind(this), 1000);

        $("#add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    showWord(word){
        $("#words", this.board).append($("<li>", {text: word}));
        }

    async handleSubmit(e){
        e.preventDefault();
        const $word = $("#word", this.board);
        let word = $word.val();

        if(!word)
            return;
        if(this.words.contains(word)){
            this.showMessage(`"${word}" already found!`)
            return;
        }

        const res = await axios.get("/check-word", {params: {word: word}});
        if(res.data.result === "not-word")
            this.showMessage(`"${word}" is not a valid word.`);
        else{
            this.showWord(word);
            this.score = score + word.length();
            this.showScore();
            this.words.add(word);
            this.showMessage(`Word added: ${word}`);
        }
        $word.val("");
    }

    showMessage(status, id){
        $("#message", this.board).text(status);
        $("#message", this.board).removeAttribute("id");
        $("#message", this.board).setAttribute("id",`message ${id}`);
    }

    async showTime(){
        $("#timer", this.board).text(this.seconds);
    }
   
    async countdown(){
        this.seconds -= 1;
        this.showTime();
        if(this.seconds === 0){
            clearInterval(this.timer);
            await this.gameScore();
        }
    }
    
    showScore(){
        $("#score", this.board).text(this.score);
    }

    async gameScore(){
        $("#add-word", this.board).hide();
       const res = await axios.post("/post-score", {score : this.score});
        if(res.data.brokenRecord)
            this.showMessage(`New Record: ${this.score}`)
        else
            this.showMessage(`Final score: ${this.score}`);
    }
}