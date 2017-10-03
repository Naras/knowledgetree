package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("districtHome")
public class DistrictHome extends EntityHome<District> {

	@In(create = true)
	StateHome stateHome;

	public void setDistrictId(DistrictId id) {
		setId(id);
	}

	public DistrictId getDistrictId() {
		return (DistrictId) getId();
	}

	public DistrictHome() {
		setDistrictId(new DistrictId());
	}

	@Override
	public boolean isIdDefined() {
		if (getDistrictId().getCountryId() == null
				|| "".equals(getDistrictId().getCountryId()))
			return false;
		if (getDistrictId().getId() == null
				|| "".equals(getDistrictId().getId()))
			return false;
		if (getDistrictId().getStateId() == null
				|| "".equals(getDistrictId().getStateId()))
			return false;
		return true;
	}

	@Override
	protected District createInstance() {
		District district = new District();
		district.setId(new DistrictId());
		return district;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		State state = stateHome.getDefinedInstance();
		if (state != null) {
			getInstance().setState(state);
		}
	}

	public boolean isWired() {
		if (getInstance().getState() == null)
			return false;
		return true;
	}

	public District getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<Address> getAddresses() {
		return getInstance() == null ? null : new ArrayList<Address>(
				getInstance().getAddresses());
	}

}
