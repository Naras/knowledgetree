package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personHasAffiliationList")
public class PersonHasAffiliationList extends EntityQuery<PersonHasAffiliation> {

	private static final String EJBQL = "select personHasAffiliation from PersonHasAffiliation personHasAffiliation";

	private static final String[] RESTRICTIONS = {
			"lower(personHasAffiliation.id.affiliation) like lower(concat(#{personHasAffiliationList.personHasAffiliation.id.affiliation},'%'))",
			"lower(personHasAffiliation.id.person) like lower(concat(#{personHasAffiliationList.personHasAffiliation.id.person},'%'))",};

	private PersonHasAffiliation personHasAffiliation;

	public PersonHasAffiliationList() {
		personHasAffiliation = new PersonHasAffiliation();
		personHasAffiliation.setId(new PersonHasAffiliationId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public PersonHasAffiliation getPersonHasAffiliation() {
		return personHasAffiliation;
	}
}
