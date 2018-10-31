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
  // True means invalid
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

      // Track whether the user just submitted the form
      successfulSubmission: false,

      // Dropdown options
      valueRequiringSpecifics: 'Other',
      numDucksOptions: ['5', '10', '15', '20', '30', '40', '50'],
      foodTypeOptionsMap: {},
      foodAmountOptions: ['25g', '50g', '100g', '200g', '500g', '1000g']
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
  componentDidMount() {
      this.getFoodOptions();
  }

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
      successfulSubmission: false
    });
  };

  /**
   * Get all food categories
   */
  getFoodOptions() {
    axios.get(`${process.env.REACT_APP_BASE_API_URL}/food/categories`)
      .then((res) => {
        let categoryMap = {};
        let categories = res.data.categories;
        for (let i=0; i < categories.length; i++) {
          let categoryName = categories[i]['name'];
          let typeNames = [];
          axios.get(`${process.env.REACT_APP_BASE_API_URL}/food/types?category_name=${encodeURIComponent(categoryName)}`)
            .then((res) => {
              let types = res.data.types;
              for (let i=0; i < types.length; i++) {
                typeNames.push(types[i]['name']);
              }
            })
            .catch((err) => { console.log(err); });

          categoryMap[categoryName] = typeNames;
        }
        this.setState({foodTypeOptionsMap: categoryMap})
      })
      .catch((err) => { console.log(err); });
  }

  /**
   * Validate form contents before submit
   */
  canBeSubmitted() {
    const errors = validate(this.state.feedingEventInfo, this.state.valueRequiringSpecifics);
    return !(errors.numberOfDucks || errors.food || errors.specificFood || errors.foodType || errors.specificFoodType || errors.amountOfFood || errors.location || errors.time);
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

    // Send to app
    e.preventDefault();
    let eventData = this.state.feedingEventInfo;
    let foodType = eventData.food === this.state.valueRequiringSpecifics ?
          eventData.specificFood
        : eventData.foodType === this.state.valueRequiringSpecifics ?
            eventData.specificFoodType
          : eventData.foodType;
    const data = {
      location_name: eventData.location,
      location_gpid: '',
      location_types: '',
      category_name: eventData.food,
      food_type: foodType,
      num_ducks: eventData.numberOfDucks,
      grams: eventData.amountOfFood.slice(0, -1),
      datetime: eventData.time
    };
    axios.post(`${process.env.REACT_APP_BASE_API_URL}/submissions`, data)
        .then((res) => { console.log(res); })
        .catch((err) => { console.log(err); });

    // Display success message and clear form data
    this.setState({successfulSubmission: true});
    this.handleClearForm(e);
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
              options = {this.state.numDucksOptions}
              value = {this.state.feedingEventInfo.numberOfDucks}
              placeholder = {'Select closest number'}
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

            { this.state.feedingEventInfo.currentFoodTypeOptions && this.state.feedingEventInfo.currentFoodTypeOptions.length > 0 ?
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

          { this.state.successfulSubmission === true ?
            <p>Form submitted successfully. Thank you for your participation.</p>
          : null } {/* Success message after submissino */}

        </form>
    );
  }
}

const buttonStyle = {
  margin : '10px 10px 10px 10px'
};

export default FormContainer;