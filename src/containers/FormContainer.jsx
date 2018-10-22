import React, {Component} from 'react';  

/* Import Components */
import Input from '../components/Input';
import Select from '../components/Select';
import Button from '../components/Button'

class FormContainer extends Component {  
  constructor(props) {
    super(props);

    this.state = {
      feedingEventInfo: {
          food: '',
          specificFood: '',
          foodType: '',
          spcificFoodType: '',
          currentFoodTypeOptions: null,
          numberOfDucks: ''
      },

      numberRangeOptions: ['1-5', '5-10', '10-15', '15-20', '20-30', '30-40', '40-50', '50+'],
      foodTypeOptionsMap: {
        'Bread' : ['White', 'Whole wheat', 'Sourdough', 'Rye'],
        'Corn' : ['Canned', 'Frozen', 'Fresh'],
        'Duck pellets': null,
        'Lettuce or other greens': [],
        'Oats' : ['Rolled', 'Instant'],
        'Peas' : ['Frozen', 'Fresh'],
        'Seeds' :  ['Bird seed', 'Other'],
        'Other' : null
      },
    };

    this.handleRange = this.handleRange.bind(this);
    this.handleFood = this.handleFood.bind(this);
    this.handleFoodType = this.handleFoodType.bind(this);
    this.handleInput = this.handleInput.bind(this);
    this.handleClearForm = this.handleClearForm.bind(this);
    this.handleFormSubmit = this.handleFormSubmit.bind(this);
  }

  /* This lifecycle hook gets executed when the component mounts */

  handleRange(e) {
       let value = e.target.value;
   this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, numberOfDucks: value
        }
      }), () => console.log(this.state.feedingEventInfo))
  }

  handleFood(e) {
    let value = e.target.value;
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, food: value
        }
    }), () => console.log(this.state.feedingEventInfo));

    this.setState( prevState => ({ feedingEventInfo :
      {...prevState.feedingEventInfo, currentFoodTypeOptions: this.state.foodTypeOptionsMap[value]
      }
    }), () => console.log(this.state.feedingEventInfo))

      // TODO clear food type value when selection changes
      // TODO make sure food type does not default to first item in the list when selection changes
      // TODO add note about deliberately not clearing "other" values
  }

  handleFoodType(e) {
    let value = e.target.value;
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, foodType: value
        }
    }), () => console.log(this.state.feedingEventInfo))

      // TODO add note about deliberately not clearing "other" values
  }

  handleInput(e) {
       let value = e.target.value;
       let name = e.target.name;
   this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, [name]: value
        }
      }), () => console.log(this.state.feedingEventInfo))
  }

  handleFormSubmit(e) {
      //TODO add some validation and sanitization
      // TODO send to app correctly
    e.preventDefault();
    let eventData = this.state.feedingEventInfo;

    fetch('http://example.com',{
        method: "POST",
        body: JSON.stringify(eventData),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
      }).then(response => {
        response.json().then(data =>{
          console.log("Successful" + data);
        })
    })
  }   

  handleClearForm(e) {
    //TODO keep updated
      e.preventDefault();
      this.setState({
        feedingEventInfo: {
          food: '',
          specificFood: '',
          foodType: '',
          spcificFoodType: '',
          currentFoodTypeOptions: null,
          numberOfDucks: ''
        },
      })
  }

  render() {
    return (
    
        <form className="container-fluid" onSubmit={this.handleFormSubmit}>

          <Select title={'Number of ducks fed'}
            name={'numberOfDucks'}
            options = {this.state.numberRangeOptions}
            value = {this.state.feedingEventInfo.numberOfDucks}
            placeholder = {'Select Number Range'}
            handleChange = {this.handleRange}
          /> {/* Duck num Selection */}

          <Select title={'Food given'}
            name={'duckFood'}
            options = {Object.keys(this.state.foodTypeOptionsMap)}
            value = {this.state.feedingEventInfo.food}
            placeholder = {'Select'}
            handleChange = {this.handleFood}
          /> {/* Duck food Selection */}

          {/* TODO only show for Other selection */}
          <Input inputType={'text'}
           title= {'Please specify'}
           name= {'specificFood'}
           value={this.state.feedingEventInfo.specificFood}
           handleChange = {this.handleInput}
          /> {/* Specific food for "Other" selection */}

          { this.state.feedingEventInfo.currentFoodTypeOptions ?
              <Select title={'Please specify'}
                name={'duckFoodType'}
                options = {this.state.feedingEventInfo.currentFoodTypeOptions}
                value = {this.state.feedingEventInfo.foodType}
                placeholder = {'Select'}
                handleChange = {this.handleFoodType}
              /> : null } {/* Specific type of food Selection */}

          {/* TODO only show for Other selection */}
          <Input inputType={'text'}
           title= {'Please specify'}
           name= {'spcificFoodType'}
           value={this.state.feedingEventInfo.spcificFoodType}
           handleChange = {this.handleInput}
          /> {/* Specific food for "Other" selection */}

          <Button 
              action = {this.handleFormSubmit}
              type = {'primary'} 
              title = {'Submit'} 
            style={buttonStyle}
          /> { /*Submit */ }
          
          <Button 
            action = {this.handleClearForm}
            type = {'secondary'}
            title = {'Clear'}
            style={buttonStyle}
          /> {/* Clear the form */}
          
        </form>
  
    );
  }
}

const buttonStyle = {
  margin : '10px 10px 10px 10px'
}

export default FormContainer;