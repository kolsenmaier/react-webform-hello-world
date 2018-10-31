import React, {Component} from 'react';
import axios from 'axios';

/* Import Components */
import Input from '../components/Input';
import Select from '../components/Select';
import Button from '../components/Button';
import CustomDateTimePicker from '../components/CustomDateTimePicker';

/**
 * Confirm fields are filled in and have valid data
 */
function validate(feedingEventInfo, valueRequiringSpecifics) {
  // true means invalid
  return {
    numberOfDucks: feedingEventInfo.numberOfDucks.length === 0,
    food: feedingEventInfo.food.length === 0,
    specificFood: feedingEventInfo.food === valueRequiringSpecifics && feedingEventInfo.specificFood.length === 0,
    foodType: feedingEventInfo.currentFoodTypeOptions != null && feedingEventInfo.foodType.length === 0,
    specificFoodType: feedingEventInfo.currentFoodTypeOptions != null && feedingEventInfo.foodType === valueRequiringSpecifics && feedingEventInfo.specificFoodType.length === 0,
    amountOfFood: feedingEventInfo.amountOfFood.length === 0,
    location: feedingEventInfo.location.length === 0,
    time: feedingEventInfo.time === null
  };
}

class FormContainer extends Component {  
  constructor(props) {
    super(props);
    this.getFoodOptions();  //TODO

    this.state = {
      // Current form entry info
      feedingEventInfo: {
        location: '',
        time: null,
        numberOfDucks: '',
        food: '',
        specificFood: '',
        foodType: '',
        specificFoodType: '',
        currentFoodTypeOptions: null,
        amountOfFood: ''
      },

      // Track whether user has had a chance to enter information before performing validation
      touched: {
        location: false,
        time: false,
        numberOfDucks: false,
        food: false,
        specificFood: false,
        foodType: false,
        specificFoodType: false,
        amountOfFood: false
      },

      // Dropdown options
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
      foodAmountOptions: ['25g', '50g', '100g', '200g', '500g', '1000g', 'More than 1000g', 'I don\'t know'],
    };

    this.handleDate = this.handleDate.bind(this);
    this.handleNumDucks = this.handleNumDucks.bind(this);
    this.handleFood = this.handleFood.bind(this);
    this.handleFoodType = this.handleFoodType.bind(this);
    this.handleFoodAmount = this.handleFoodAmount.bind(this);
    this.handleInput = this.handleInput.bind(this);
    this.handleClearForm = this.handleClearForm.bind(this);
    this.handleFormSubmit = this.handleFormSubmit.bind(this);
  }

  /* This lifecycle hook gets executed when the component mounts */

  /**
   * Handle datetime picker
   */
  handleDate(e) {
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, time: e}
    }), () => console.log(this.state.feedingEventInfo));
  }

  /**
   * Handle selection of the number of ducks
   */
  handleNumDucks(e) {
    let value = e.target.value;
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, numberOfDucks: value}
    }), () => console.log(this.state.feedingEventInfo));
  }

  /**
   * Handle the food selection. This influences the specific food field and food type selection.
   * We do not clear specific food/type fields when selection changes. Form submission handles that logic.
   */
  handleFood(e) {
    let value = e.target.value;
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, food: value}
    }), () => console.log(this.state.feedingEventInfo));

    // Clear any selected food type value since we're about to set a new list of options
    this.setState( prevState => ({ feedingEventInfo :
      {...prevState.feedingEventInfo, foodType: ''}
    }), () => console.log(this.state.feedingEventInfo));

    // Set new food type options based on the selected food
    this.setState( prevState => ({ feedingEventInfo :
      {...prevState.feedingEventInfo, currentFoodTypeOptions: this.state.foodTypeOptionsMap[value]}
    }), () => console.log(this.state.feedingEventInfo));
  }

  /**
   * Handle selection of food type. This influences whether we want a specific food type entry.
   * We do not clear specific food type fields when selection changes. Form submission handles that logic.
   */
  handleFoodType(e) {
    let value = e.target.value;
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, foodType: value}
    }), () => console.log(this.state.feedingEventInfo));
  }

  /**
   * Handle selection of the amount of food
   */
  handleFoodAmount(e) {
      let value = e.target.value;
      this.setState( prevState => ({ feedingEventInfo :
          {...prevState.feedingEventInfo, amountOfFood: value}
      }), () => console.log(this.state.feedingEventInfo));
  }

  /**
   * Handle generic input fields.
   * We do not sanitize this input here. Form submission handles that logic.
   */
  handleInput(e) {
    let value = e.target.value;
    let name = e.target.name;
    this.setState( prevState => ({ feedingEventInfo :
        {...prevState.feedingEventInfo, [name]: value}
    }), () => console.log(this.state.feedingEventInfo));
  }

  /**
   * Track whether the user has focused the field
   */
  handleBlur = (field) => (e) => {
    this.setState({
      touched: { ...this.state.touched, [field]: true },
    });
  };

  /**
   * Get all food categories
   */
  getFoodOptions() {
    axios.get(`${process.env.REACT_APP_BASE_API_URL}/food/categories`)
      .then((res) => { console.log(res.data.categories); }) //TODO
      .catch((err) => { console.log(err); });
  }

  /**
   * Validate form contents before submit
   */
  canBeSubmitted() {
    const errors = validate(this.state.feedingEventInfo, this.state.valueRequiringSpecifics);
  }

  /**
   * Perform basic validation of form fields and submit contents to the app via fetch POST
   */
  handleFormSubmit(e) {
    if (!this.canBeSubmitted()) {
      e.preventDefault();
      // Show errors in all currently visible required fields
      this.setState({
        touched: {
          location: true,
          time: true,
          numberOfDucks: true,
          food: true,
          specificFood: this.state.feedingEventInfo.food === this.state.valueRequiringSpecifics,
          foodType: this.state.feedingEventInfo.food.length !== 0 && this.state.feedingEventInfo.food !== this.state.valueRequiringSpecifics,
          specificFoodType: this.state.feedingEventInfo.foodType === this.state.valueRequiringSpecifics,
          amountOfFood: true
        },
      });
      return;
    }
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

  /**
   * Clear form fields and reset focus tracking
   */
  handleClearForm(e) {
      e.preventDefault();
      this.setState({
        feedingEventInfo: {
          location: '',
          time: null,
          numberOfDucks: '',
          food: '',
          specificFood: '',
          foodType: '',
          specificFoodType: '',
          currentFoodTypeOptions: null,
          amountOfFood: ''
        },

        touched: {
          location: false,
          time: false,
          numberOfDucks: false,
          food: false,
          specificFood: false,
          foodType: false,
          specificFoodType: false,
          amountOfFood: false
        },
      })
  }

  render() {
    const errors = validate(this.state.feedingEventInfo, this.state.valueRequiringSpecifics);

    return (

        <form className="container-fluid" onSubmit={this.handleFormSubmit}>
          <p>Required fields are followed by <abbr title="required"> *</abbr>.</p>

          <fieldset>
            <legend>General information</legend>

            <Input inputType={'text'} title={'Location'}
              name={'location'}
              required={true}
              value = {this.state.feedingEventInfo.location}
              placeholder = {'Enter the location you fed the ducks'}
              hasErrors={errors.location && this.state.touched.location}
              handleBlur={this.handleBlur('location')}
              handleChange = {this.handleInput}
            /> {/* Location input */}

            <CustomDateTimePicker title={'Time'}
              name={"time"}
              required={true}
              value={this.state.feedingEventInfo.time}
              hasErrors={errors.time && this.state.touched.time}
              handleBlur={this.handleBlur('time')}
              handleChange={this.handleDate}
            /> {/* Datetime picker */}

            <Select title={'Number of ducks'}
              name={'numberOfDucks'}
              required={true}
              options = {this.state.numberRangeOptions}
              value = {this.state.feedingEventInfo.numberOfDucks}
              placeholder = {'Select number range'}
              hasErrors={errors.numberOfDucks && this.state.touched.numberOfDucks}
              handleBlur={this.handleBlur('numberOfDucks')}
              handleChange = {this.handleNumDucks}
            /> {/* Duck num Selection */}

          </fieldset>

          <fieldset>
            <legend>Food given</legend>

            <Select title={'Type of food'}
              name={'food'}
              required={true}
              options = {Object.keys(this.state.foodTypeOptionsMap)}
              value = {this.state.feedingEventInfo.food}
              placeholder = {'Select'}
              hasErrors={errors.food && this.state.touched.food}
              handleBlur={this.handleBlur('food')}
              handleChange = {this.handleFood}
            /> {/* Duck food Selection */}

            { this.state.feedingEventInfo.food === this.state.valueRequiringSpecifics ?
            <Input inputType={'text'} title={'Please specify'}
              name={'specificFood'}
              required={true}
              value={this.state.feedingEventInfo.specificFood}
              hasErrors={errors.specificFood && this.state.touched.specificFood}
              handleBlur={this.handleBlur('specificFood')}
              handleChange={this.handleInput}
            /> : null } {/* Specific food for "Other" selection */}

            { this.state.feedingEventInfo.currentFoodTypeOptions ?
            <Select title={'Please specify'}
              name={'foodType'}
              required={true}
              options = {this.state.feedingEventInfo.currentFoodTypeOptions}
              value = {this.state.feedingEventInfo.foodType}
              placeholder = {'Select'}
              hasErrors={errors.foodType && this.state.touched.foodType}
              handleBlur={this.handleBlur('foodType')}
              handleChange = {this.handleFoodType}
            /> : null } {/* Specific type of food Selection */}

            { this.state.feedingEventInfo.foodType === this.state.valueRequiringSpecifics ?
            <Input inputType={'text'} title= {'Please provide details'}
              name= {'specificFoodType'}
              required={true}
              value={this.state.feedingEventInfo.specificFoodType}
              hasErrors={errors.specificFoodType && this.state.touched.specificFoodType}
              handleBlur={this.handleBlur('specificFoodType')}
              handleChange = {this.handleInput}
            /> : null } {/* Specific food for "Other" selection */}

            <Select title={'Amount'}
              name={'amountOfFood'}
              required={true}
              options = {this.state.foodAmountOptions}
              value = {this.state.feedingEventInfo.amountOfFood}
              placeholder = {'Select your best estimate in grams'}
              hasErrors={errors.amountOfFood && this.state.touched.amountOfFood}
              handleBlur={this.handleBlur('amountOfFood')}
              handleChange = {this.handleFoodAmount}
            /> {/* Food amount Selection */}

          </fieldset>

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
};

export default FormContainer;