package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("addressList")
public class AddressList extends EntityQuery<Address> {

	private static final String EJBQL = "select address from Address address";

	private static final String[] RESTRICTIONS = {
			"lower(address.id) like lower(concat(#{addressList.address.id},'%'))",
			"lower(address.area) like lower(concat(#{addressList.address.area},'%'))",
			"lower(address.houseNumber) like lower(concat(#{addressList.address.houseNumber},'%'))",
			"lower(address.street) like lower(concat(#{addressList.address.street},'%'))",
			"lower(address.value) like lower(concat(#{addressList.address.value},'%'))",};

	private Address address = new Address();

	public AddressList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Address getAddress() {
		return address;
	}
}
