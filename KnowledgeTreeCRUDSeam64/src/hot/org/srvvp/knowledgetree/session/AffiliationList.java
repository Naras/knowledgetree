package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("affiliationList")
public class AffiliationList extends EntityQuery<Affiliation> {

	private static final String EJBQL = "select affiliation from Affiliation affiliation";

	private static final String[] RESTRICTIONS = {
			"lower(affiliation.id) like lower(concat(#{affiliationList.affiliation.id},'%'))",
			"lower(affiliation.name) like lower(concat(#{affiliationList.affiliation.name},'%'))",};

	private Affiliation affiliation = new Affiliation();

	public AffiliationList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Affiliation getAffiliation() {
		return affiliation;
	}
}
