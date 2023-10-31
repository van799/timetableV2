   document.addEventListener('DOMContentLoaded', function() {
     var Calendar = FullCalendar.Calendar;
     var Draggable = FullCalendar.Draggable;

     var containerEl = document.getElementById('external-events');
     var calendarEl = document.getElementById('calendar');
     var checkbox = document.getElementById('drop-remove');


     // initialize the external events
     // -----------------------------------------------------------------

     new Draggable(containerEl, {
       itemSelector: '.fc-event',
       eventData: function(eventEl) {
         return {
           title: eventEl.innerText
         };
       }
     });

     // initialize the calendar
     // -----------------------------------------------------------------

     var calendar = new Calendar(calendarEl, {
      locale: "ru",
       firstDay: 1,
       height: "100",
       initialView: "dayGridMonth",

       headerToolbar: {
         left: 'prev,next today',
         center: 'title',
         right: 'dayGridMonth,timeGridDay'

       },
      events : [
                {% for event in events %}
                    {
                    title : '{{event.todo}}',
                    start : '{{event.date}}',
                    },
                {% endfor %}
                ],
              editable: true,
      droppable: true,
    eventReceive: function(info) {

     //get the bits of data we want to send into a simple object
     var eventData = {
       title: info.event.title,
       start: info.event.startStr,
       end: info.event.end
     };
     console.log(eventData);
     //send the data via an AJAX POST request, and log any response which comes from the server
     fetch('insert', {
         method: 'POST',
         headers: {
           'Accept': 'application/json'
         },
         body: encodeFormData(eventData),
         dataType : 'json'
       })
       .then(response => console.log(response))
       .catch(error => console.log(error));
   },

    eventDrop: function(info) {

     //get the bits of data we want to send into a simple object
     var eventData = {
       old_title: info.oldEvent.title,
       old_start: info.oldEvent.startStr,

       title: info.event.title,
       start: info.event.startStr,
     };
     console.log(eventData);
     //send the data via an AJAX POST request, and log any response which comes from the server
     fetch('update', {
         method: 'POST',
         headers: {
           'Accept': 'application/json'
         },
         body: encodeFormData(eventData),
         dataType : 'json'
       })
       .then(response => console.log(response))
       .catch(error => console.log(error));
   }


 });
 calendar.render();
});

const encodeFormData = (data) => {
  var form_data = new FormData();

  for (var key in data) {
    form_data.append(key, data[key]);
  }
  return form_data;
}