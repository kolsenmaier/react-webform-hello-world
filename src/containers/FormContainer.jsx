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
        numberOfDucks: '',
        food: '',
        specificFood: '',
        foodType: '',
        specificFoodType: '',
        currentFoodTypeOptions: null
      },

      valueRequiringSpecifics: 'Other',
      numberRangeOptions: ['1-5', '5-10', '10-15', '15-20', '20-30', '30-40', '40-50', '50+'],
      foodTypeOptionsMap: {
        'Bread' : ['White', 'Whole wheat', 'Sourdough', 'Rye', 'Other'],
        'Corn' : ['Canned', 'Frozen', 'Fresh'],
        'Duck pellets': null,
        'Lettuce or other greens': null,
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

  /**
   * Handle the food selection. This influences the specific food field and food type selection.
   * We do not clear specific food/type fields when selection changes and let the POST handle that logic instead.
   */
  handleFood(e) {
    let value = e.target.value;
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, food: value
        }
    }), () => console.log(this.state.feedingEventInfo));

    // Clear any selected food type value since we're about to set a new list of options
    this.setState( prevState => ({ feedingEventInfo :
      {...prevState.feedingEventInfo, foodType: ''
      }
    }), () => console.log(this.state.feedingEventInfo));

    // Set new food type options based on the selected food
    this.setState( prevState => ({ feedingEventInfo :
      {...prevState.feedingEventInfo, currentFoodTypeOptions: this.state.foodTypeOptionsMap[value]
      }
    }), () => console.log(this.state.feedingEventInfo));

      // TODO make sure food type does not default to first item in the list when selection changes
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
          numberOfDucks: '',
          food: '',
          specificFood: '',
          foodType: '',
          specificFoodType: '',
          currentFoodTypeOptions: null
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

          { this.state.feedingEventInfo.food == this.state.valueRequiringSpecifics ?
            <Input inputType={'text'}
               title={'Please specify'}
               name={'specificFood'}
               value={this.state.feedingEventInfo.specificFood}
               handleChange={this.handleInput}
            /> : null } {/* Specific food for "Other" selection */}

          { this.state.feedingEventInfo.currentFoodTypeOptions ?
              <Select title={'Please specify'}
                name={'duckFoodType'}
                options = {this.state.feedingEventInfo.currentFoodTypeOptions}
                value = {this.state.feedingEventInfo.foodType}
                placeholder = {'Select'}
                handleChange = {this.handleFoodType}
          /> : null } {/* Specific type of food Selection */}

          { this.state.feedingEventInfo.foodType == this.state.valueRequiringSpecifics ?
              <Input inputType={'text'}
               title= {'Please specify'}
               name= {'specificFoodType'}
               value={this.state.feedingEventInfo.specificFoodType}
               handleChange = {this.handleInput}
          /> : null } {/* Specific food for "Other" selection */}

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