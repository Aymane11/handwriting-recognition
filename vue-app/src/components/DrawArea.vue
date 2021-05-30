<template>
    <div class="draw-area-container">
        <canvas id="draw-area"></canvas>
        <div class="container draw-area-footer">
            <div>
                <button @click.prevent="clearDrawArea" class="clear-area-button">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
                <button @click.prevent="undoLastMove" class="undo-button">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                    </svg>
                </button>
            </div>
            <button @click.prevent="readImage" class="predict-image-button">Predict the image</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    props: {
        drawColor: {
            type: String,
            required: false,
            default: "#000",
        },
        drawWidth: {
            type: Number,
            required: false,
            default: 20,
        }
    },

    data () {
        return {
            canvas: null,
            context: null,
            painting: false,
            history: [],
        };
    },
    
    methods: {
        clearDrawArea () {
            this.context.fillStyle = "white";
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

            this.history = [];
        },

        undoLastMove () {
            let index = this.history.length - 1;
            if (index <= 0) {
                this.clearDrawArea();
            } else {
                this.history.pop();
                this.context.putImageData(this.history[index-1], 0, 0);
            }
        },

        start (event) {
            this.painting = true;

            this.context.beginPath();
            this.context.lineTo(event.clientX - this.canvas.offsetParent.offsetLeft, 
                event.clientY - this.canvas.offsetParent.offsetTop);
                
            event.preventDefault();
        },

        stop (event) {
            if (this.painting) {
                this.context.stroke();
                this.context.closePath();
            }
            
            this.painting = false;
            
            if (event.type != 'mouseout') {
                this.history.push(this.context.getImageData(0, 0, this.canvas.width, this.canvas.height));
            }

            event.preventDefault();
        },

        draw (event) {
            if (! this.painting)
                return;
            
            this.context.lineTo(event.clientX - this.canvas.offsetParent.offsetLeft, 
                event.clientY - this.canvas.offsetParent.offsetTop);
            
            this.context.strokeStyle = this.drawColor;
            this.context.lineWidth = this.drawWidth;
            this.context.lineCap =  "round";
            this.context.lineJoin = "round";
            this.context.stroke();

            event.preventDefault();
        },

        async readImage () {
            console.log(this.canvas.toDataURL('image/jpeg', 1.0));
            try {
                let response = await axios.get('https://api.coindesk.com/v1/bpi/currentprice.json')
                console.log(response.data.bpi)
            } catch (e) {

            } finally {

            }
        },
    },
    
    mounted () {
        // window.addEventListener("load", () => {
        this.canvas = document.querySelector("#draw-area"); 
        this.context = this.canvas.getContext("2d"); 
            
        // Resizing the canvas
        this.canvas.height = this.canvas.parentElement.offsetHeight - 2;

        this.canvas.width = this.canvas.parentElement.offsetWidth - 2;

        // First style
        this.clearDrawArea();

        this.canvas.addEventListener("touchstart", this.start);
        this.canvas.addEventListener("touchend", this.stop);
        this.canvas.addEventListener("touchmove", this.draw);
            
        this.canvas.addEventListener("mousedown", this.start);
        this.canvas.addEventListener("mouseup", this.stop);
        this.canvas.addEventListener("mouseout", this.stop);
        this.canvas.addEventListener("mousemove", this.draw);   

        // TODO: EventListener resize maybe later
    }
}
</script>