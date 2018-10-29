import React from 'react';

const Input = (props) => {
	return (  
      <div className="form-group">
        <label htmlFor={props.name} className="form-label">{props.title}{props.required ? <abbr title="required"> *</abbr> : ''}</label>
        <input
          className="form-control"
          id={props.name}
          name={props.name}
          type={props.inputType}
          value={props.value}
          onBlur={props.handleBlur}
          onChange={props.handleChange}
          placeholder={props.placeholder}
          style={props.hasErrors ? customerror : null}
          {...props} />
      </div>
    )
};

const customerror = {
    border: '3px solid salmon'
};

export default Input;