package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personWorkRelationHome")
public class PersonWorkRelationHome extends EntityHome<PersonWorkRelation> {

	public void setPersonWorkRelationId(String id) {
		setId(id);
	}

	public String getPersonWorkRelationId() {
		return (String) getId();
	}

	@Override
	protected PersonWorkRelation createInstance() {
		PersonWorkRelation personWorkRelation = new PersonWorkRelation();
		return personWorkRelation;
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

	public PersonWorkRelation getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<PersonHasWork> getPersonHasWorks() {
		return getInstance() == null ? null : new ArrayList<PersonHasWork>(
				getInstance().getPersonHasWorks());
	}

}
