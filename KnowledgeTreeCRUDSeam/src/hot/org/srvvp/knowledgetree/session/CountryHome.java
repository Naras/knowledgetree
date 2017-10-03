package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("countryHome")
public class CountryHome extends EntityHome<Country> {

	public void setCountryId(String id) {
		setId(id);
	}

	public String getCountryId() {
		return (String) getId();
	}

	@Override
	protected Country createInstance() {
		Country country = new Country();
		return country;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public Country getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<State> getStates() {
		return getInstance() == null ? null : new ArrayList<State>(
				getInstance().getStates());
	}

}
