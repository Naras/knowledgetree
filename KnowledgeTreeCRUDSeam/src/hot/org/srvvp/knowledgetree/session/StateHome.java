package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("stateHome")
public class StateHome extends EntityHome<State> {

	@In(create = true)
	CountryHome countryHome;

	public void setStateId(StateId id) {
		setId(id);
	}

	public StateId getStateId() {
		return (StateId) getId();
	}

	public StateHome() {
		setStateId(new StateId());
	}

	@Override
	public boolean isIdDefined() {
		if (getStateId().getCountryId() == null
				|| "".equals(getStateId().getCountryId()))
			return false;
		if (getStateId().getId() == null || "".equals(getStateId().getId()))
			return false;
		return true;
	}

	@Override
	protected State createInstance() {
		State state = new State();
		state.setId(new StateId());
		return state;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Country country = countryHome.getDefinedInstance();
		if (country != null) {
			getInstance().setCountry(country);
		}
	}

	public boolean isWired() {
		if (getInstance().getCountry() == null)
			return false;
		return true;
	}

	public State getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<City> getCities() {
		return getInstance() == null ? null : new ArrayList<City>(getInstance()
				.getCities());
	}
	public List<District> getDistricts() {
		return getInstance() == null ? null : new ArrayList<District>(
				getInstance().getDistricts());
	}

}
