import React from 'react';
import DateTimePicker from 'react-datetime-picker';
import './react-datetime.css';

const CustomDateTimePicker = (props) => {
    return(<div className="form-group rdt">
      <label htmlFor={props.name}> {props.title}{props.required ? <abbr title="required"> *</abbr> : ''}</label><br/>
      <DateTimePicker
        id = {props.name}
        name={props.name}
        className={props.hasErrors ? 'customerror' : null}
        value={props.value}
        clearIcon={null}
        disableClock={true}
        onBlur={props.handleBlur}
        onChange={props.handleChange}
      />
    </div>)
};

export default CustomDateTimePicker;