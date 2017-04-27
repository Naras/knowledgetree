package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("districtList")
public class DistrictList extends EntityQuery<District> {

	private static final String EJBQL = "select district from District district";

	private static final String[] RESTRICTIONS = {
			"lower(district.id.countryId) like lower(concat(#{districtList.district.id.countryId},'%'))",
			"lower(district.id.id) like lower(concat(#{districtList.district.id.id},'%'))",
			"lower(district.id.stateId) like lower(concat(#{districtList.district.id.stateId},'%'))",
			"lower(district.name) like lower(concat(#{districtList.district.name},'%'))",};

	private District district;

	public DistrictList() {
		district = new District();
		district.setId(new DistrictId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public District getDistrict() {
		return district;
	}
}
