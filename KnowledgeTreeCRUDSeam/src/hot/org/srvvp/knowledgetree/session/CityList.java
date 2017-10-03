package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("cityList")
public class CityList extends EntityQuery<City> {

	private static final String EJBQL = "select city from City city";

	private static final String[] RESTRICTIONS = {
			"lower(city.id.countryId) like lower(concat(#{cityList.city.id.countryId},'%'))",
			"lower(city.id.id) like lower(concat(#{cityList.city.id.id},'%'))",
			"lower(city.id.stateId) like lower(concat(#{cityList.city.id.stateId},'%'))",
			"lower(city.name) like lower(concat(#{cityList.city.name},'%'))",};

	private City city;

	public CityList() {
		city = new City();
		city.setId(new CityId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public City getCity() {
		return city;
	}
}
