import React from 'react';

const Select = (props) => {
	return(<div className="form-group customerror">
			<label htmlFor={props.name}> {props.title}{props.required ? <abbr title="required"> *</abbr> : ''}</label>
		    <select
		      id = {props.name}
		      name={props.name}
		      value={props.value}
			  onBlur={props.handleBlur}
		      onChange={props.handleChange}
		      className="form-control"
			  style={props.hasErrors ? customerror : null}>
		      <option value="" disabled>{props.placeholder}</option>
		      {props.options.map(option => {
		        return (
		          <option
		            key={option}
		            value={option}
		            label={option}>{option}</option>
		        );
		      })}
		    </select>
	  </div>
	)
};

const customerror = {
    border: '3px solid salmon'
};

export default Select;