const socketcortina = io();
            var cons='x';
            
            
            socketcortina.emit('cortina','SO','x')
            
            console.log(cons);
            
            var Emerger = document.querySelector(".Emergente");
            
                
            
           
            var cerro= document.querySelector(".Cerrar");
            socketcortina.on('id2',function (estadocortina,raton) {
                
                cons='1';
                if(raton=='NO'){
                    
                    console.log('No entraste a opciones');
                    if (estadocortina=='Abierto'){
                        $('.CortinaSemi').css('display','none');
                        $('.CortinaCerrada').css('display','none');
                        $('.CortinaAbierta').css('display','flex');
                        $('#cajacortina').empty();
                        $('#cajacortina').append('<div class="CortinaAbierta"> </div>');
                        $('.CortinaAbierta').on('click',function(){
                            socketcortina.emit('cortina','SI','x')
                            $('.Emergente').css('display','flex');
                        })


                    }
                    if (estadocortina=='Cerrado'){
                        $('.CortinaSemi').css('display','none');
                        $('.CortinaCerrada').css('display','flex');
                        $('.CortinaAbierta').css('display','none');
                        $('#cajacortina').empty();
                        $('#cajacortina').append('<div class="CortinaCerrada"> </div>');
                        $('.CortinaCerrada').on('click',function(){
                            socketcortina.emit('cortina','SI','x')
                            $('.Emergente').css('display','flex');
                        })

                    }
                    if (estadocortina=='Semi'){
                        $('.CortinaSemi').css('display','flex');
                        $('.CortinaCerrada').css('display','none');
                        $('.CortinaAbierta').css('display','none');
                        $('#cajacortina').empty();
                        $('#cajacortina').append('<div class="CortinaSemi"> </div>');                        
                        $('.CortinaSemi').on('click',function(){
                            socketcortina.emit('cortina','SI','x')
                            $('.Emergente').css('display','flex');
                        })
                    }
                }
                if (raton=='SI'){
                    console.log('presionaste');
                    
                    $('#arriba').on('click',function () {
                            console.log('sube');

                        socketcortina.emit('cortina','SI','subiendo');
                    })

                     $('#abajo').on('click',function () {


                        socketcortina.emit('cortina','SI','bajando');
                    })
                     $('#cerrar').on('click',function () {


                        socketcortina.emit('cortina','SI','cerrando');
                    })
                     $('#abrir').on('click',function () {


                        socketcortina.emit('cortina','SI','abriendo');
                    })
                    //si tocas fuerade la puta ventana  reactjs promesa!
                /*    function windowOnClick(event) {
                if (event.target === Emerger) {
                    $('.Emergente').css('display','none');
                    //socketcortina.emit('cortina','NO','x');
                }
                }
                    window.addEventListener("click", windowOnClick);*/
                   
                    $('.Cerrar').on("click", function() {
                        socketcortina.emit('parar');
                       console.log('cerraste');
                       //emitir que se cerro para q deje de leer los sensores
                       $('.Emergente').css('display','none');
                       
                      socketcortina.emit('cortina','NO','x');
                    
                      document.location.reload(true);
                      
                   })

                }
              

                    
                    
                
            })

            const socket = io();
            const socket2=io();
        socket2.emit('luz','');
            
            
            
               socket.on('id',function (estado) {
                   console.log(estado)
                   if (estado=='Encendido') {
                       $('.centroEncendido').css('display','flex');
                       $('.centroApagado').css('display','none');
                       $('#caja').empty();
                       $('#caja').append('<div class="centroEncendido"> </div>');
                       $('.centroEncendido').on('click',function(){
                             socket.emit('luz','Apagar');
                            
                        })
                   }
                   else
                   {
                       
                       if (estado== 'Apagado') {
                        $('.centroEncendido').css('display','none');
                       $('.centroApagado').css('display','flex');
                       $('#caja').empty();
                        $('#caja').append('<div class="centroApagado"> </div>');
                        $('.centroApagado').on('click',function(){
                            socket.emit('luz','Encender');
                        })
                       }
                   }
                
                   
               }) 


$(document).on("click", "#presionar", function(){
    console.log(" Presionado");
    $.ajax({
        url: "http://localhost:5000/abrir",
        type: "GET",
        error: function(){
            console.log("Error al lla,ar el metodo")
        },
        success: function(e){
            console.log("respuesta: "+ e);
        }
     });
})